# Phase 1: Classify Repository

**[State Checkpoint]**
- MUST verify the `Target Directory` absolute path passed from the previous step.
- MUST navigate to the `Target Directory` BEFORE proceeding.

## [Discovery Phase: Environment Validation]
1. VCS Detection: MUST execute native checks (e.g., `git status` or checking for `.git/`) to determine if the `Target Directory` is under Version Control.
   - IF it is a Git repository, MUST locate and acknowledge the `.gitignore` file to establish the absolute boundaries of relevant files. MUST NOT rely on manual directory exclusion lists.
2. Dynamic Environment Check: IF unknown configuration files (e.g., `.unknown-ci.yml`) are present at the root, MUST perform web research or use internal knowledge to identify their purpose BEFORE making archetype assumptions.

## [Elimination & Evaluation Phase]
3. Archetype Matching: 
   - IF `package.json` or `pyproject.toml` exists, archetype IS `code`.
   - IF `docker-compose.yml` or `pnpm-workspace.yaml` exists, archetype IS `product`.
   - IF `SKILL.md` exists at root, archetype IS `single-skill`.
   - IF `skills/` directory exists, archetype IS `multi-skills`.
   - IF `mkdocs.yml` or `_sidebar.md` exists, archetype IS `docs`.
   - IF multiple signals match, archetype IS `hybrid`.
4. Anomaly Handling: IF NO signals match, MUST NOT guess. MUST ask the user via `vscode_askQuestions` to determine the archetype.

## [Record: Handoff]
5. State Packaging: MUST explicitly record the identified `archetype`, the `Target Directory`, and the `VCS Status` (e.g., Git repository, tracking confirmed).
6. Handoff: MUST execute `workflows/02-recon.md` and explicitly pass these variables forward.
