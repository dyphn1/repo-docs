# repo-docs

> Automatically generate or update README.md and AGENTS.md based on a repository's actual file structure and configuration files. Works across code, products, and AI skill libraries.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Writing and maintaining documentation is a tedious task that quickly falls out of sync with the codebase. The `repo-docs` skill solves this by acting as an intelligent technical writer. It analyzes your repository's structure (whether it's a Monorepo, a SaaS product, a single AI skill, or a massive multi-skill library) and automatically generates two distinct files:
- **`README.md`**: Tailored for human readers, focusing on value propositions, quick starts, and usage workflows.
- **`AGENTS.md`**: Tailored for AI agents, providing strict rules, architectures, commands, and formatting constraints.

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

When invoked, the skill executes a multi-step intelligent process:

1. **Zoom Out: Classify Archetype**: The AI looks at the top-level structure to determine if your project is `code`, `product`, `single-skill`, `multi-skills`, `courseware`, or `docs`.
2. **Multi-layered Reconnaissance**: Based on the archetype, it fires off specialized Python scripts (`recon_core.py`, `recon_workspace.py`, etc.) to extract languages, dependencies, monorepo boundaries, and even deeply embedded semantic docs (like GitBook quick starts).
3. **Smart Restructure & Merge**: If you already have docs, it doesn't just append to them. It extracts "developer commands" out of the README and moves them into `AGENTS.md`, while bringing "user guides" into the README.
4. **Generate README**: Uses an archetype-specific template to craft a human-readable guide.
5. **Generate AGENTS**: Uses an archetype-specific template to craft a strict AI authoring/development guide.

*(See the `SKILL.md` file for the exact machine-readable instructions.)*

---

## Key Rules & Constraints

- **Never Invent Facts**: Every generated claim must come from a readable file. Missing data is marked with `{{TODO}}` instead of being hallucinated.
- **Audience Segregation**: Content strictly useful for AI agents (exact compilation commands, constraints, gotchas) belongs in `AGENTS.md`. Human-facing prose stays in `README.md`.
- **Archetype Awareness**: The skill dynamically alters the sections it generates based on the detected repository type (e.g., a SaaS product gets a "Typical Use Cases" section; a multi-skill library gets a "Categorized Skills Index").

---

## Resources & File Structure

This skill utilizes supplementary context files and scripts to guide its behavior:

```
.
├── SKILL.md                   # Core AI instructions and workflow definition
├── references/                # The layout templates for different archetypes
│   ├── readme-template.md                 # Base README guide
│   ├── agents-template.md                 # Base AGENTS guide
│   ├── product-readme-template.md         # Template for SaaS/Products
│   ├── product-agents-template.md         # Developer guide for Products
│   ├── single-skill-readme-template.md    # Template for single-skill repos
│   ├── multi-skills-readme-template.md    # Template for multi-skill libraries
│   ├── skills-agents-template.md          # Meta-authoring guide for modifying skills
│   └── manual-recon.md                    # Fallback bash commands
└── scripts/                   # Multi-layered reconnaissance toolkit
    ├── recon_core.py          # Extracts languages, package managers, tree
    ├── recon_code.py          # Extracts dependencies, scripts, CI commands
    ├── recon_docs.py          # Semantic extraction of GitBook/Wiki headers
    ├── recon_workspace.py     # Detects monorepo boundaries (apps vs libs)
    └── recon_skills.py        # Extracts skill categories, dependencies, and examples
```

---

## Contributing

Open a PR to update the templates in `references/` or enhance the reconnaissance capabilities in `scripts/`. When adding support for a new archetype, update the signals table in `SKILL.md`.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
