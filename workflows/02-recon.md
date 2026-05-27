# Phase 2: Reconnaissance

MUST run the appropriate Python scripts to gather context based on the archetype.

## Execution Steps

1. IF archetype IS `code`, `product`, or `hybrid`:
   1. MUST execute `python scripts/recon_workspace.py <target_dir>`.
   2. MUST execute `python scripts/recon_code.py <target_dir>`.
2. IF archetype IS `single-skill` or `multi-skills`:
   1. MUST execute `python scripts/recon_skills.py <target_dir>`.
3. IF archetype IS `courseware` or `docs`:
   1. MUST execute `python scripts/recon_docs.py <target_dir>`.
4. IF any Python script fails, MUST fallback to native `read_file` to inspect files.
5. MUST read existing `README.md` and `AGENTS.md` using `read_file`.
6. MUST extract human-written tutorials and save them as `PRESERVED_HUMAN_CONTENT`.
7. MUST correlate the extracted data (e.g. identify dependencies or navigation trees).
8. MUST execute `workflows/03-generate.md`.
