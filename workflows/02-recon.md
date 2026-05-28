# Phase 2: Reconnaissance

## Core Principles
- MUST execute steps one by one.
- MUST NOT combine terminal commands (e.g., using `&&` or `;`).
- MUST NOT skip steps or assume outcomes without checking.

## Execution Steps

1. MUST execute `python scripts/recon_workspace.py <target_dir>` IF `code` or `product`.
2. MUST execute `python scripts/recon_skills.py <target_dir>` IF `single-skill` or `multi-skills`.
3. IF `recon_workspace.py` reports `unrecognized_directories`, MUST use native tools to check them.
4. MUST read existing `README.md` and `AGENTS.md` using `read_file`.
5. MUST extract existing detailed content (Architecture, Constraints) into `PRESERVED_HUMAN_CONTENT`.
6. MUST deeply analyze the target `SKILL.md` (and sub-workflows) using `read_file` IF archetype is skill-based.
7. MUST extract actual execution pipeline, phase logic, and strict constraints into `SKILL_LOGIC_SUMMARY`.
8. MUST correlate all extracted data.
9. MUST execute `workflows/03-draft.md`.

Next: Execute `workflows/03-draft.md`
