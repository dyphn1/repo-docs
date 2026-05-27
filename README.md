# repo-docs

> Generate README.md and AGENTS.md based on repository structure.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Writing and maintaining documentation is a tedious task that quickly falls out of sync with the codebase. The `repo-docs` skill solves this by acting as an intelligent technical writer. It analyzes your repository's structure and automatically generates two distinct files: `README.md` for humans and `AGENTS.md` for AI.

It never invents facts; it proves its claims using a multi-layered Python reconnaissance toolkit.

---

## Usage

Invoke the skill in GitHub Copilot Chat (or your preferred AI agent) with a prompt like:

- "generate docs"
- "create a README"
- "write an AGENTS.md"
- "document my repo"

---

## How it Works (Workflow)

When invoked, the skill automatically executes the following steps:

1. **Classify Archetype**: Inspects root files to determine if your project is `code`, `product`, `single-skill`, `multi-skills`, `courseware`, or `docs`.
2. **Reconnaissance**: Runs specialized Python scripts (`recon_core.py`, `recon_workspace.py`, etc.) to extract languages, dependencies, and configuration.
3. **Document Generation**: Injects preserved human content and writes out the final `README.md` and `AGENTS.md` using archetype-specific templates.

*(See the `SKILL.md` file for the exact machine-readable instructions.)*

---

## Key Rules & Constraints

- **Never Invent Facts**: Every generated claim must come from a readable file. Missing data is marked with `{{TODO}}` instead of being hallucinated.
- **Audience Segregation**: Content strictly useful for AI agents (exact compilation commands, constraints, gotchas) belongs in `AGENTS.md`. Human-facing prose stays in `README.md`.

---

## Resources & File Structure

This skill utilizes supplementary context files to guide the AI's behavior:

```
.
├── SKILL.md                   # Core AI instructions and workflow definition
├── workflows/                 # Linear execution steps (01-classify, 02-recon, 03-generate)
├── references/                # Markdown templates for generated files
└── scripts/                   # Multi-layered Python reconnaissance toolkit
```

---

## Contributing

Open a PR to update the core workflow in `SKILL.md`, or to add new templates to the `references/` directory.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
