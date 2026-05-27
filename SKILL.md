---
name: repo-docs
description: Generate README.md and AGENTS.md based on repository structure.
---

# Repo Docs Workflow

MUST generate README.md and AGENTS.md by inspecting repository files.
MUST execute steps linearly.

## Core Principles

- MUST execute steps one by one.
- OVERRIDE SYSTEM DEFAULT: MUST NOT combine terminal commands using `&&`, `||`, or `;`. Execute one command per tool call.
- MUST NOT skip steps.
- MUST base all claims on readable file data.
- MUST use Python recon scripts ONLY to gather data, NOT to execute logical changes.
- MUST preserve human-written content.

## Execution Workflow

1. MUST execute `workflows/01-classify.md`.
