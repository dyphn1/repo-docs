# Phase 1: Classify Repository

MUST determine the repository archetype by inspecting root files.

## Execution Steps

1. MUST use native tools (`file_search`, `read_file`) to check root files.
2. IF `package.json`, `Cargo.toml`, or `pyproject.toml` exists, archetype IS `code`.
3. IF `docker-compose.yml` or `pnpm-workspace.yaml` exists, archetype IS `product`.
4. IF `SKILL.md` exists at root, archetype IS `single-skill`.
5. IF `skills/` directory exists, archetype IS `multi-skills`.
6. IF `exercises/` directory exists, archetype IS `courseware`.
7. IF `mkdocs.yml` or `_sidebar.md` exists, archetype IS `docs`.
8. IF multiple signals match, archetype IS `hybrid`.
9. IF NO signals match, MUST ask the user using `vscode_askQuestions`.
10. MUST log the identified archetype.
11. MUST execute `workflows/02-recon.md`.
