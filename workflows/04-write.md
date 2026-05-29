# Phase 4: Finalize and Write

**[State Checkpoint]**
- MUST verify the finalized draft strings for `README.md` and `AGENTS.md` passed from Phase 3.
- MUST ensure terminal is located at the `Target Directory`.

## [Summarize: Final Validation]
1. Content Review: MUST review the final drafted content in memory.
2. Separation of Concerns: MUST verify human-readable and agent-readable content are fully separated.
3. Constraint Check: MUST verify all strict rules and architectural specs are intact.

## [Action Phase: User Consent]
4. Authorization: MUST present a summary of the final drafted content to the user for confirmation via `vscode_askQuestions`.
5. Disk Write: MUST write the final `README.md` and `AGENTS.md` to the `Target Directory` ONLY IF the user explicitly approves.

## [Record: Exit]
6. Completion: MUST log success, declare the new documentation state, and terminate execution.

[Exit: Await User Instruction]
