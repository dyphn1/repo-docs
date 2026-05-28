# Phase 2: Reconnaissance

MUST run the appropriate Python scripts to gather context based on the archetype.

## Core Principles

- MUST execute steps one by one.
- MUST NOT combine terminal commands (e.g., using `&&` or `;`).
- MUST NOT skip steps or assume outcomes without checking.

## Execution Steps

1. IF archetype IS `code`, `product`, or `hybrid`:
   1. MUST execute `python scripts/recon_workspace.py <target_dir>`.
   2. MUST execute `python scripts/recon_code.py <target_dir>`.
2. IF archetype IS `single-skill` or `multi-skills`:
   1. MUST execute `python scripts/recon_skills.py <target_dir>`.
3. IF archetype IS `courseware` or `docs`:
   1. MUST execute `python scripts/recon_docs.py <target_dir>`.
4. IF `recon_workspace.py` reports `unrecognized_directories`, MUST use native `ls`, `find` to check their purpose.
5. IF any Python script fails, MUST fallback to native `read_file` to inspect files.
6. MUST read existing `README.md` and `AGENTS.md` using `read_file`.
7. MUST extract human-written tutorials and save them as `PRESERVED_HUMAN_CONTENT`.
8. MUST correlate extracted data (e.g. identify dependencies or unassigned folders).
9. MUST execute `workflows/03-generate.md`.
