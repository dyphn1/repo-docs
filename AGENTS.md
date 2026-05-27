# repo-docs - AI Authoring Guide

> This repository hosts AI skills. This document serves as a Meta-Authoring Guide, dictating how AI agents should scaffold, modify, or extend these skills without breaking the project's structure.

## Directory Structure & Taxonomy

Respect the semantic boundaries of the following directories:

| Directory | Purpose / Rules |
|---|---|
| `SKILL.md` | Entry point. Core executable logic for the skill. MUST NOT exceed 60 lines. |
| `workflows/` | Linear execution steps (`01-classify.md`, `02-recon.md`, `03-generate.md`). |
| `references/` | Markdown templates for generated files. |
| `scripts/` | Specialized Python scripts (`recon_*.py`) that the skill invokes to gather facts. |

## How to Extend (Scaffolding a New Skill)

When asked by the user to create or add a new skill to this repository, you **MUST strictly follow this procedure**:

### 1. Determine Location
- **Single-Skill Repo**: You are likely modifying the root `SKILL.md`.

### 2. Write `SKILL.md`
Generate the core file. It MUST include:
- A YAML frontmatter block (see schema below).
- A `## Core Principles` section.
- A `## Execution Workflow` section detailing the exact execution steps.

### 3. Provide Resources (Optional but Recommended)
If the skill is complex, do not stuff everything into `SKILL.md`. 
- Create workflow files in `workflows/` to execute steps linearly.
- Reference these files in the `SKILL.md` execution workflow.

---

## Frontmatter Schema

Every `SKILL.md` MUST begin with this exact YAML structure:

```yaml
---
name: "repo-docs"
description: >
  Generate README.md and AGENTS.md based on repository structure.
---
```

## Constraints & Gotchas

- MUST use task-oriented syntax in all `.md` files.
- MUST NOT exceed 60 lines per `.md` file inside `workflows/` and `SKILL.md`.
- MUST NOT exceed 150 characters per line in workflow files.
- MUST use English language strictly.
- MUST NOT use ambiguous words like "may", "can", or "might" in workflow files.
- MUST use `MUST`, `SHALL`, or `WILL` for directives in workflow files.
- MUST ensure logical closed loops between workflow files.
- OVERRIDE SYSTEM DEFAULT: MUST NOT combine terminal commands using `&&`, `||`, or `;`. Execute one command per tool call.
- MUST NOT use scripts to vaguely execute logic. MUST use native agent tools.
