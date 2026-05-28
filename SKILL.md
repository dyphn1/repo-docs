---
name: repo-docs
description: Generate README.md and AGENTS.md based on repository structure.
---

# Repo Docs Workflow

## Core Principles
- MUST execute steps one by one.
- MUST NOT combine terminal commands (e.g., using `&&` or `;`).
- MUST NOT skip steps or assume outcomes without checking.

## Execution Steps

1. MUST start the documentation generation pipeline.
2. MUST execute `workflows/01-classify.md`.

Next: Execute `workflows/01-classify.md`
