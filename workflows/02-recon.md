# Phase 2: Reconnaissance

**[State Checkpoint]**
- MUST verify the `Target Directory` and `archetype` passed from Phase 1.
- MUST ensure terminal is located at the `Target Directory`.

## [Action Phase: Scripted & Native Recon]
1. Deterministic Scanning: MUST attempt to execute the corresponding python script to gather structural data securely:
   - IF `code` or `product`: MUST execute `python scripts/recon_workspace.py <target_dir>`.
   - IF `single-skill` or `multi-skills`: MUST execute `python scripts/recon_skills.py <target_dir>`.
   - IF `hybrid` OR ambiguous: MUST use `vscode_askQuestions` to clarify priority, or safely execute both scripts if contextually appropriate.
2. Graceful Degradation (Fallback): IF scripts crash, are unavailable, or the environment is alien, MUST abandon single-pass tools. Instead, MUST perform Iterative Native Reconnaissance (e.g., `ls -la`) to build the mental map layer by layer.
3. Dynamic Verification & Zero-Trust: For ANY `unrecognized_directories` OR standard directories (e.g., `docs/`) discovered via scripts or native recon:
   - MUST NOT trust directory names implicitly. MUST perform shallow sampling (e.g., viewing root contents of `docs/`) to verify its true nature (e.g., simple markdown vs. massive React site).
   - IF a directory's purpose remains unknown, MUST perform web research to determine its relevance.
   - IF deemed irrelevant or private (e.g., `.cache`, personal notes), MUST explicitly discard it.
4. Dynamic Abstraction (Anti-Bloat): IF discovering massive homogenous structures (e.g., 50 microservices), MUST NOT exhaustively scan. MUST sample 2-3 instances, abstract the common architecture, and record a high-level summary to strictly protect Context limits.

## [Discovery Phase: Content Extraction]
3. Legacy & Deep Content: MUST read existing `README.md`, `AGENTS.md`, and any highly relevant files discovered inside previously unrecognized directories (e.g., AI profiles in `.claude/`) securely.
4. Human Context: MUST extract existing detailed content (Architecture, Constraints, Dynamic Discoveries) into a state variable named `PRESERVED_HUMAN_CONTENT`.
5. Skill Logic: IF archetype is skill-based, MUST deeply analyze the target `SKILL.md` (and sub-workflows) securely. MUST extract actual execution pipeline, phase logic, and strict constraints into a state variable named `SKILL_LOGIC_SUMMARY`.

## [Record: Handoff]
6. State Packaging: MUST correlate all extracted data.
7. Handoff: MUST execute `workflows/03-draft.md` and explicitly pass `Target Directory`, `archetype`, `PRESERVED_HUMAN_CONTENT`, and `SKILL_LOGIC_SUMMARY`.
