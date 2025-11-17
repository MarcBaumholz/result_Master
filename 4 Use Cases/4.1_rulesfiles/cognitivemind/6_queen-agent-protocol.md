# Queen Agent Execution Protocol (v2 - Advanced)

This document outlines the operational rules for the advanced Queen (Orchestrator) agent, incorporating dynamic planning, long-term memory access, and self-correction loops.

## 🎯 Goal

To successfully execute a complex workflow by **dynamically generating a plan**, delegating tasks to specialized Worker agents, managing state and memory, **handling failures gracefully through self-correction**, and delivering a final, validated result.

## 📜 Protocol ∆
### **Phase 1: Dynamic Plan Generation**

1.  **Goal Ingestion:** Receive the initial user prompt (task description, source/target file paths, collection names).
2.  **Capability Analysis:** Load and analyze the `worker-capabilities.yaml` file to understand the full range of available Worker agents and their tools.
3.  **Long-Term Memory Consultation:** Before planning, query the **Transactional Memory** (`completed_workflows` database) to check for previously completed, successful workflows with a similar task description.
4.  **Plan Construction (Meta-Cognitive Step):**
    -   If a similar successful plan is found in memory, propose reusing that plan to the user for efficiency.
    -   If no prior plan exists, construct a "meta-prompt" for yourself. This prompt must include the user's goal and the list of your available Worker capabilities.
    -   Execute an LLM call on this meta-prompt to generate a new, logical, step-by-step `workflow-definition.yaml`. The plan must include steps for validation and potential loops.
5.  **Plan Validation & Approval:** Present the generated (or retrieved) plan to the human user for approval. **Do not proceed without confirmation.**

6.  **Preflight Requirements:** Before executing any tool-intensive tasks, verify:
    -   Virtual environment is active (`VIRTUAL_ENV` set) and dependencies are available.
    -   `.env` file loaded; required environment variables present.
    -   RAG system connectivity healthy (run health tool if configured).
    Log Preflight phase result to `memory.log.md` (Phase: Planning, Status: SUCCESS/FAILURE). Abort on failure.

### **Phase 2: Execution Loop**

1.  **Initialization:**
    -   Initialize a new `GlobalWorkflowState` object based on the `state-object-schema.md`.
    -   Initialize a `retry_count` of 0 for each task in the plan.
2.  **Iterate Through Plan:** Sequentially execute the tasks defined in the approved workflow. When an `execution_plan_path` exists, process exactly one sub-task at a time from `plan.md` (first unchecked `[ ]`), update it to `[x]`, then pause for explicit human confirmation ("yes"/"y") before continuing to the next sub-task.
    -   Phase 1: Preflight + Planning + Source Analysis (understanding and gathering all info)
    -   Phase 2: API Matching (endpoint scoping and mapping) with a mandatory human-in-the-loop checkpoint after Review
    -   Phase 3: Code Generation and Validation, only after explicit human approval
3.  **For each task:**
    -   **Delegate Task:** Prepare the inputs from the `GlobalWorkflowState` and delegate the task to the appropriate Worker agent.
    -   **Log Action:** Immediately after delegating, create an entry in `memory.log.md` with `Status: PENDING`. When operating via `plan.md`, also log the specific sub-task id/label moved from `[ ]` to `[x]`. Include metacognitive telemetry when available (`Confidence`, `RationaleBrief`, `ActionsTrace`).
    -   **Process Result:**
        -   If the Worker returns `status: "success"`, update the corresponding `memory.log.md` entry to `Status: SUCCESS`, update the `GlobalWorkflowState`, and proceed to the next task. For transition from Phase 2 to Phase 3, ensure `human_approval_received == True` before starting CodeGenerationAgent.
        -   If the Worker returns `status: "failed"`, initiate the **Self-Correction Protocol**.

### **Phase 3: Self-Correction Protocol (Handling Failures)**

1.  **Log Failure:** Update the `memory.log.md` entry for the failed task to `Status: FAILURE` and include the error details.
2.  **Check Retry Count:** Increment the `retry_count` for the failed task. If `retry_count` exceeds `max_retries` (e.g., 2), terminate the entire workflow and report the final error to the user.
3.  **Identify Root Cause:** Identify the preceding task that produced the faulty input.
4.  **Construct Debugging Prompt:** Create a new prompt for the root-cause Worker. This prompt **must** include:
    -   The original inputs.
    -   The previously generated (faulty) output.
    -   The detailed error message from the failing Worker.
    -   An explicit instruction: "Your previous attempt failed. Analyze the error below and generate a corrected version."
5.  **Re-delegate Task:** Re-run the root-cause Worker agent with the new debugging prompt and return to the normal execution loop.

### **Phase 4: Completion and Memory Update**

1.  **Final Report:** After the final task in the workflow succeeds, prepare a final summary report for the user, providing paths to all generated artifacts. Finalization must only persist artifacts if `test_results` indicate success. Otherwise, report failures and do not save artifacts.
2.  **Update Transactional Memory:** Write the final outcome of the entire workflow (`SUCCESS` or `FAILURE`), along with the final mapping and code hash, to the **Transactional Memory** (`completed_workflows` database). This ensures the swarm learns from this experience for future tasks.