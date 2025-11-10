# Cognitive Mind Architecture Overview (API Connector Swarm)

This document outlines the high-level architecture for the API Connector Generation swarm. It is the central reference point for understanding how the system operates.

## 🏛️ Core Concepts

This system is composed of a central orchestrator (the "Queen") and a set of specialized, independent "Worker" agents, forming a cognitive-mind architecture.

1.  **The Queen Agent (Orchestrator):** This is the central brain of the operation. It is initiated by the user (e.g., via a Cursor command). It interprets the `workflow-definition.yaml` to create a plan, delegates tasks to the appropriate Worker agents, and manages the `GlobalWorkflowState`. It also logs all significant events to `memory.log.md`.

2.  [cite_start]**Worker Agents (Specialists):** Each Worker is an expert in a single domain, corresponding to the MCP tools in your project[cite: 66, 1]. The specifications for each worker are detailed in `worker-agent-specifications.md`.

3.  **The Global State Object:** A single, shared data object that holds the context for the *current* integration task. Its structure is defined in `state-object-schema.md`.

4.  **The Workflow Definition:** A declarative YAML file (`workflow-definition.yaml`) that defines the sequence of tasks, which Worker performs each task, and how data flows between them. [cite_start]This plan is derived directly from your documented workflow[cite: 1, 10].

5.  **Long-Term Memory:** A persistent log file (`memory.log.md`) that records the outcome of every tool execution. This provides a traceable history of the swarm's actions and learnings, as defined in `memory-protocol.md`.

## ⚙️ High-Level Workflow

[Developer in Cursor] -> [@runIntegrationWorkflow]
|
V
[Queen Agent] reads [workflow-definition.yaml]
|
+-> [Worker A] -> Logs to [memory.log.md] -> Updates [State]
|
+-> [Worker B] -> Logs to [memory.log.md] -> Updates [State]
|
... (pauses for human approval)
|
V
[Final Artifacts]