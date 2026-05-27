# Phase 3: Document Generation

MUST generate and write the final README.md and AGENTS.md.

## Execution Steps

1. MUST select templates from `references/` based on archetype.
2. IF `code` or `hybrid`, MUST use `readme-template.md` and `agents-template.md`.
3. IF `product`, MUST use `product-readme-template.md` and `product-agents-template.md`.
4. IF `single-skill`, MUST use `single-skill-readme-template.md` and `skills-agents-template.md`.
5. IF `multi-skills`, MUST use `multi-skills-readme-template.md` and `skills-agents-template.md`.
6. IF `docs` or `courseware`, MUST use `knowledge-readme-template.md` and `knowledge-agents-template.md`.
7. MUST inject `PRESERVED_HUMAN_CONTENT` into the README.
8. MUST separate developer commands into the AGENTS file.
9. MUST wait for user confirmation before writing.
10. MUST write final `README.md` and `AGENTS.md`.
11. MUST terminate execution.
