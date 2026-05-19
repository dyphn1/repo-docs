# repo-docs

A GitHub Copilot Chat Skill that generates or refreshes `README.md` and `AGENTS.md` by inspecting a repo's actual file structure and config files. Uses a seven-step workflow: classify archetype → gather context → determine scope → generate README → generate AGENTS.md → write files → verify. Supports `code`, `skills`, `courseware`, `docs`, and `hybrid` archetypes.

## Workflows & Commands

### Run recon on a repo (code archetype)
```bash
python scripts/recon.py <repo_root>
# Outputs JSON: directory tree, detected project type, build/test/lint commands, entry points
```

### Update a template
```bash
# Edit references/readme-template.md or references/agents-template.md directly.
# Templates are plain Markdown — no build step needed.
```

### Extend archetype support
```bash
# 1. Add archetype signals to the table in SKILL.md (Step 0 — Archetype signals)
# 2. Add a gathering branch in SKILL.md (Step 1 — archetype-specific section)
# 3. Add the section set row to references/readme-template.md (Archetype-Aware table)
# 4. Add the commands block to references/agents-template.md (Non-Code Archetype Templates)
```

## Skills Inventory

| Field | Value |
|---|---|
| `name` | `repo-docs` |
| `description` | Automatically generate or update README.md and AGENTS.md for any repo type. |
| Reference files | `references/agents-template.md`, `references/manual-recon.md`, `references/readme-template.md` |
| Scripts | `scripts/recon.py` (code archetype recon) |

## File Layout

```
SKILL.md                             # Skill entry point — seven-step workflow
references/
  readme-template.md                 # Archetype-aware README.md template
  agents-template.md                  # Archetype-aware AGENTS.md template
  manual-recon.md                    # Bash commands for manual recon (no Python)
scripts/
  recon.py                           # Automated recon for code archetype repos
```

## Authoring Rules

- **Frontmatter** must have `name` and `description`. Description should match the trigger phrases users will say (e.g., "generate docs", "create a README").
- **Templates** in `references/` use `{placeholder}` syntax (single braces). All placeholders must be replaced with real values from config files when generating output — never emit a bare `{placeholder}` literal.
- **`{{TODO: ...}}` markers** (double braces) are emitted in *output* when data is unavailable. They are not template placeholders — do not remove them from SKILL.md without a substitute.
- **`recon.py`** is only invoked for the `code` archetype. All other archetypes use direct file reading per the Step 1 branch in SKILL.md.
- **Source citations**: every generated documentation section must note which file(s) it was derived from, to keep output verifiable.
- **Preserve human content**: when updating existing README or AGENTS.md, keep prose, screenshots, badges, and custom sections intact. Only refresh auto-detectable sections.

## Frontmatter Schema

```yaml
---
name: "{skill-name}"       # kebab-case
description: >             # trigger phrases the user would say
  Automatically generate or update ...
---
```

## Do Not Edit

- The `## Full Template (code archetype)` block in `references/readme-template.md` — canonical section set parsed by the skill.
- The output schema of `scripts/recon.py` — JSON keys are referenced by name in SKILL.md Step 1 (`code` branch).
- `{{TODO: ...}}` patterns in `SKILL.md` — these are intentional output markers, not authoring placeholders.
