# repo-docs

A GitHub Copilot Chat Skill that automatically generates or updates `README.md` and `AGENT.md` based on a repository's actual file structure and configuration files.

> **AI agents:** Read [`AGENT.md`](AGENT.md) for skill structure, archetype classification rules, template conventions, and authoring guidance before making changes.

---

## Overview

`repo-docs` inspects a repo's file tree and config files, then produces accurate, verifiable documentation — with no invented facts. It handles code projects (Node, Python, .NET, Rust, Go, monorepos), AI skill libraries, educational courseware, and documentation sites. When updating existing files, it preserves human-written content and only refreshes auto-detectable sections (commands, versions, file structure). Missing data is marked with `{{TODO: ...}}` rather than silently omitted.

---

## Skills

| Name | Description |
|---|---|
| `repo-docs` | Automatically generate or update README.md and AGENT.md based on a repository's current file structure and configuration files. Works with any repo type: code projects (Node, Python, .NET, Rust, Go, monorepo), AI skill libraries, educational courseware, documentation sites, or hybrids. |

---

## Usage

Invoke the skill in GitHub Copilot Chat with a prompt like:

- "generate docs"
- "create a README"
- "write an AGENT.md"
- "update project docs"
- "document my repo"

The skill classifies the repository archetype, gathers context from config files, and writes or updates `README.md` and `AGENT.md` at the repo root.

---

## File Structure

```
.
├── LICENSE                          # Apache 2.0
├── README.md                        # This file
├── SKILL.md                         # Skill definition with seven-step workflow
├── references/
│   ├── agent-template.md            # AGENT.md template with archetype-specific sections
│   ├── manual-recon.md              # Manual recon commands when recon.py is unavailable
│   └── readme-template.md           # README.md template with archetype-specific sections
└── scripts/
    └── recon.py                     # Reconnaissance script for code archetype repos
```

---

## Contributing

Open a PR to update the templates in `references/` or the recon script in `scripts/`. When adding support for a new archetype, update both the archetype signal table in `SKILL.md` (Step 0) and the section-set tables in both reference templates.

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.