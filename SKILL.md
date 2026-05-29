---
name: repo-docs
description: Generate README.md and AGENTS.md based on repository structure.
---

# Repo Docs Workflow

## Core Principles
- MUST operate using the cognitive loop: Think > Try > Summarize > Record.
- [Think] MUST build a holistic mental router map before starting. Use elimination to discard impossible approaches. Perform forward prediction to simplify actions.
- [Try] MUST verify current environment boundaries BEFORE taking action. Execute steps sequentially and NEVER combine commands, ensuring errors remain isolated and traceable.
- [Summarize] MUST verify actual outcomes against initial intent; hallucinating success is forbidden. If an attempt fails, diagnose, zoom out, and backtrack.
- [Record] MUST explicitly state variables and context to carry over.
- [Reflect & Re-Think] MUST actively feed the `[Record]` (especially past failures and state changes) back into the next `[Think]` cycle. Use historical context to refine forward predictions and strictly avoid repeating previously diagnosed errors.

## Cognitive Foundation (Why we do this)
- Recording is not the end; it is the absolute prerequisite for the next Think cycle.
- Trying validates the predicted steps.
- Summarizing confirms if the outcome aligns with the initial intent.
- The loop is continuous. Converging the chain of thought is the absolute priority; divergent thinking causes attention loss. This cycle (Think > Try > Summarize > Record > Re-Think) drives self-adaptation and evolution.
- Treat these rules as strict guardrails. Autonomous optimization within these boundaries is expected.

## [State Checkpoint]
- MUST verify the Target Directory provided by the user. IF missing, MUST verify if the current working directory is the intended Target Directory.
- MUST explicitly record the absolute path of the Target Directory.

## Execution Workflow

1. **[Think: Scope Planning]**: MUST understand the pipeline: Classify -> Reconnaissance -> Draft -> Finalize.
2. **[Record: Handoff]**: MUST execute `workflows/01-classify.md`, explicitly passing the `Target Directory` absolute path as the starting context.
