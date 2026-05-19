# repo-docs - AI Authoring Guide

> This repository hosts a single AI skill (`repo-docs`) equipped with a multi-layered Python reconnaissance toolkit and various markdown templates. This document serves as a Meta-Authoring Guide, dictating how AI agents should modify or extend this skill.

## Directory Structure & Taxonomy

Respect the semantic boundaries of the following directories:

| Directory | Purpose / Rules |
|---|---|
| `SKILL.md` | The core executable logic for the skill. It controls the classification logic and workflow steps. |
| `references/` | Markdown templates that dictate the structure of generated README and AGENTS files. Contains archetype-specific files (e.g., `product-*`, `skills-*`). |
| `scripts/` | Specialized Python scripts (`recon_*.py`) that the skill invokes to gather facts about the target repository. |

## How to Extend (Scaffolding / Modifying)

When asked by the user to modify or extend this skill, you **MUST strictly follow this procedure**:

### 1. Adding Support for a New Archetype
If asked to support a new repository type (e.g., "game engine"):
- **Update `SKILL.md`**: Add the new archetype to the "Archetype signals" and "Forced clarification" tables in Step 0.
- **Add Templates**: Create a new `{archetype}-readme-template.md` and `{archetype}-agents-template.md` in the `references/` folder.
- **Update Master Indexes**: Modify `references/readme-template.md` and `references/agents-template.md` to map the new archetype to your new templates.

### 2. Modifying Reconnaissance Logic
If asked to make the skill detect new things (e.g., "detect if it uses GraphQL"):
- **Modify Scripts**: Edit the appropriate Python script in `scripts/` (e.g., `recon_code.py` for dependencies, or `recon_core.py` for config files).
- **Update SKILL.md**: If the new logic requires a new script, ensure you add the execution command to Step 1 of `SKILL.md`.

### 3. Modifying Output Templates
If asked to change what the generated README/AGENTS files look like:
- Edit the corresponding files in the `references/` directory.
- **NEVER** use `{}` for placeholders. Always use `{placeholder}` if it's meant to be replaced, or `{{TODO: ...}}` for missing data markers.

---

## Frontmatter Schema

`SKILL.md` MUST begin with this exact YAML structure:

```yaml
---
name: "repo-docs"
description: >
  Automatically generate or update README.md and AGENTS.md based on a repository's...
---
```
*(Note: Unlike some skills, repo-docs does not currently utilize a `resources` array in its frontmatter, as it loads references dynamically based on the detected archetype).*

## Constraints & Gotchas

- **Python Scripts Execution**: The skill relies entirely on the `python scripts/recon_*.py` commands working on the user's machine. Do not introduce dependencies that require `pip install`; stick to the Python standard library (`os`, `sys`, `json`, `re`, `pathlib`).
- **Preservation Principle**: The core rule of this skill is to preserve human-written content. Ensure any workflow changes in `SKILL.md` maintain the "Smart Restructure & Merge" logic.
