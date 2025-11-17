# Worker Agent Specifications

This document defines the roles, inputs, and outputs for each specialized Worker agent in the hive. [cite_start]Each agent is a wrapper around one or more MCP tools from your `server_fast.py`[cite: 63].

---

### 1. **RAGManagerAgent**

-   **Purpose:** Manages the RAG knowledge base by uploading and verifying API specifications.
-   [cite_start]**MCP Tools Used:** `upload_api_specification`, `list_available_api_specs`[cite: 63].
-   **Input:** `source_spec_path`, `target_spec_path`, `source_collection_name`, `target_collection_name` from the Global State.
-   **Output:** `rag_setup_complete` (boolean) and `rag_collections` (list) added to the Global State.

---

### 2. **SourceAnalysisAgent**

-   [cite_start]**Purpose:** Performs a detailed analysis of the source JSON data to identify all relevant fields for mapping[cite: 17].
-   [cite_start]**MCP Tool Used:** `analyze_json_fields_with_rag`[cite: 65].
-   **Input:** `source_json_path`, `source_collection_name` from the Global State.
-   **Output:** `source_field_analysis_path` (the path to the generated `.md` analysis file) added to the Global State.

---

### 3. **MappingAgent**

-   [cite_start]**Purpose:** Performs an intensive, multi-strategy search to find the best matches for each source field in the target API specification, including endpoint scoping[cite: 20, 28]. Implements metacognition (confidence tracking, uncertainty flags) and CoT/ReAct traces. Additionally outputs a machine-readable `mapping.json`. Executes a mandatory Tree‑of‑Thought (ToT) triangulation across all three search strategies and produces a comparison artifact.
-   [cite_start]**MCP Tools Used:** `analyze_json_fields_with_rag`, `query_api_specification`, `enhanced_rag_analysis`, `get_direct_api_mapping_prompt`[cite: 64, 65, 63].
-   **Input:** `source_field_analysis_path`, `target_spec_path`, `target_collection_name`, `user_task_description`, `agent_confidence_threshold` from the Global State.
-   **Output:** `field_mapping_report_path` (the path to the detailed mapping report), `mapping_json_path` (machine-readable mapping), `triangulation_summary_path` (per‑field consensus/mismatch table), `field_confidences`, `uncertainty_flags`, `rationale_briefs`, and `actions_trace` added to the Global State.

---

### 4. **ReviewAgent**

-   [cite_start]**Purpose:** Performs a final cognitive review of the generated mapping, identifies any unmapped fields, and generates creative solutions; verifies claimed endpoints against the OpenAPI spec and writes an endpoints verification artifact[cite: 45]. [cite_start]It presents its findings to the human user for final approval[cite: 49]. Also runs comprehensive API verification prior to review.
-   **MCP Tools Used:** `reasoning_agent` (comprehensive orchestration and cognitive review).
-   **Input:** `field_mapping_report_path`, `target_spec_path`, `triangulation_summary_path` from the Global State.
-   **Output:** `verification_report_path`, `verification_passed`, and `human_approval_received` added to the Global State.

---

### 5. **CodeGenerationAgent**

-   [cite_start]**Purpose:** Generates clean, robust, and tested Kotlin connector code based on the user-validated mapping and a template file[cite: 49, 52].
-   [cite_start]**MCP Tool Used:** `generate_kotlin_mapping_code`[cite: 65].
-   **Input:** `field_mapping_report_path` from the Global State.
-   **Output:** `generated_kotlin_code_path` (the path to the final `.kt` file) added to the Global State.

---

### 5.1 **KotlinGeneratorAgent** (CONSOLIDATED - Phase 3)

-   **Purpose:** End-to-end Kotlin code generation including Controller, Service, and Mapper layers with security, logging, and null-safety.
-   **MCP Tool Used:** `phase3_generate_mapper`.
-   **Input:** `field_mapping_report_path`, `output_directory` from the Global State.
-   **Output:** `kotlin_mapper_code_path` (path to generated Kotlin file), `generated_components` (list: Controller/Service/Mapper), `security_annotations` (boolean) added to the Global State.

---

### 5.2 **QualityAssuranceAgent** (CONSOLIDATED - Phase 3)

-   **Purpose:** Performs rule-based code audit and generates comprehensive TDD test suites following Test-Driven Development principles.
-   **MCP Tool Used:** `phase3_quality_suite`.
-   **Input:** `kotlin_mapper_code_path`, `field_mapping_report_path`, `output_directory` from the Global State.
-   **Output:** `quality_audit_report_path`, `tdd_test_suite_path`, `audit_score` (float), `test_coverage_summary` (dict) added to the Global State.

---

### 5.3 **ConsistencySelectorAgent** (CONSOLIDATED - Phase 3)

-   **Purpose:** Selects the best Kotlin code candidate from multiple generated versions using consistency principles and heuristics.
-   **MCP Tool Used:** `phase3_select_best_candidate`.
-   **Input:** `kotlin_candidate_files` (list), `field_mapping_report_path` from the Global State.
-   **Output:** `best_candidate_path`, `selection_rationale`, `consistency_score` (float) added to the Global State.

---

### 6. **ValidationAgent**


---

### 7. **PlanningAgent**

-   **Purpose:** Creates and maintains an execution plan (`plan.md`) with parent tasks, detailed sub-tasks, and a "Relevant API Elements" manifest. Updates checkboxes as sub-tasks complete. Captures BDI context (Beliefs/Desires/Intentions) for transparency.
-   **MCP Tool Used:** None (plan is written to disk by the agent; may call documentation helpers).
-   **Input:** `source_spec_path`, `target_spec_path`, `user_task_description`, `output_directory`, optionally an existing `execution_plan_path` to update.
-   **Output:** `execution_plan_path` and `beliefs_summary`/`desires`/`intentions_checklist` added to the Global State. Also generates a short `guidelines_digest.md` from local learnings and writes its path to `guidelines_digest_path` in the Global State.

---

### 8. **ClarificationAgent**

-   **Purpose:** Identifies ambiguities in mapping/specs and asks numbered clarifying questions. Persists the user's decisions for downstream workers.
-   **MCP Tool Used:** None.
-   **Input:** `field_mapping_report_path`, `execution_plan_path`.
-   **Output:** `clarifications` (key decisions) added to the Global State.

---

### 9. **ArtifactSaverAgent**

-   **Purpose:** Finalizes and saves integration artifacts only when tests pass.
-   **MCP Tool Used:** None.
-   **Input:** `execution_plan_path`, `field_mapping_report_path`, `mapping_json_path`, `generated_kotlin_code_path`, `test_results`, `user_task_description`, `output_directory`.
-   **Output:** `integration_directory`, `integration_spec_path` (README), `mapping_json_path` (confirmed), and persisted `plan.md` under `/integrations/[source]-to-[target]/`.
-   [cite_start]**Purpose:** Compiles and runs unit tests against the generated Kotlin code using mock data from the source JSON file[cite: 54].
-   **MCP Tool Used:** This worker does not use an MCP tool. It invokes the Kotlin compiler and testing framework (e.g., JUnit) via a system command.
-   **Input:** çgenerated_kotlin_code_path`, `source_json_path` from the Global State.
-   **Output:** `test_results` (a summary of test outcomes) added to the Global State.


sd 3_workflow-definition.yaml'


---

### 0. **PreflightAgent**

-   **Purpose:** Runs preflight checks per `mcp-rules.mdc`: validates virtual environment, `.env` presence, logging setup, and RAG system connectivity before proceeding.
-   **MCP Tool Used:** `test_rag_system` (optional based on configuration).
-   **Input:** `output_directory` from the Global State.
-   **Output:** `preflight_ok` (boolean) added to the Global State.

---

### 10. **MemoryReportAgent**

-   **Purpose:** Appends a Phase Summary Report to `memory.log.md` after each major phase (1, 2, 3), aggregating key artifacts, confidences, clarifications, runtime/token usage, and (if available) evaluation metrics.
-   **MCP Tool Used:** None (writes directly to `memory.log.md` using the Memory Protocol).
-   **Input:** `phase_number`, `execution_plan_path`, `field_mapping_report_path`, `mapping_json_path`, `clarifications`, optional `test_results` and evaluation metrics from the Global State.
-   **Output:** `N/A` (side effect: a new Phase Summary log entry).

---

### 11. **LearningReportAgent**

-   **Purpose:** After successful Phase 3 completion (tests green), generates a `LEARNINGS.md` file capturing: key learnings, encountered errors and resolutions, do’s and don’ts, and improvement suggestions for future runs.
-   **MCP Tool Used:** None.
-   **Input:** `integration_directory`, `memory_log_path`, `test_results`, `mapping_report_path`, `clarifications`.
-   **Output:** `learnings_path` (absolute path to `LEARNINGS.md`) added to the Global State.
