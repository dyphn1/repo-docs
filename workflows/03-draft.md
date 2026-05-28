# Phase 3: Draft Content

## Core Principles
- MUST execute steps one by one.
- MUST NOT combine terminal commands (e.g., using `&&` or `;`).
- MUST NOT skip steps or assume outcomes without checking.

## Execution Steps

1. MUST select templates from `references/` based on archetype.
2. MUST perform Smart Merge (智慧合併) of `PRESERVED_HUMAN_CONTENT`, `SKILL_LOGIC_SUMMARY`, and Templates.
3. MUST draft human-readable `README.md` containing workflows, architecture, and value proposition.
4. MUST draft agent-readable `AGENTS.md` containing strict rules, logic models, and authoring constraints.
5. MUST NOT degrade original quality or use vague placeholders.
6. MUST compare the drafted files against the original files.
7. MUST fix any missing context or logic gaps identified during comparison.
8. MUST execute `workflows/04-write.md`.

Next: Execute `workflows/04-write.md`
