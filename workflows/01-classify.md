# Phase 1: Classify Repository

## Core Principles
- MUST execute steps one by one.
- MUST NOT combine terminal commands (e.g., using `&&` or `;`).
- MUST NOT skip steps or assume outcomes without checking.

## Execution Steps

1. MUST check root files to determine the repository archetype.
2. IF `package.json` or `pyproject.toml` exists, archetype IS `code`.
3. IF `docker-compose.yml` or `pnpm-workspace.yaml` exists, archetype IS `product`.
4. IF `SKILL.md` exists at root, archetype IS `single-skill`.
5. IF `skills/` directory exists, archetype IS `multi-skills`.
6. IF `mkdocs.yml` or `_sidebar.md` exists, archetype IS `docs`.
7. IF multiple signals match, archetype IS `hybrid`.
8. IF NO signals match, MUST ask the user via `vscode_askQuestions`.
9. MUST log the identified archetype.
10. MUST execute `workflows/02-recon.md`.

Next: Execute `workflows/02-recon.md`
