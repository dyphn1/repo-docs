---
name: repo-docs
description: >
  Automatically generate or update README.md and AGENTS.md based on a repository's
  current file structure and configuration files. Works with any repo type: code
  projects (Node, Python, .NET, Rust, Go, monorepo), AI skill libraries, educational
  courseware, documentation sites, or hybrids. Use this skill whenever the user asks
  to "generate docs", "create a README", "write an AGENTS.md", "update project docs",
  or "document my repo" — for any project type, not just code.
---

# Repo Docs Skill

Generates or updates `README.md` and `AGENTS.md` by inspecting the repo's real
file structure and configuration files — no guessing, no hallucinating project
details.

---

## Core Principles

- **Never invent facts.** Every command, version number, path, or claim must come
  from a readable file. If data is missing, use `{{TODO: <description and how to verify>}}`
  and tell the user how to fill it in.
- **Preserve human-written content.** When updating existing files, keep prose,
  screenshots, badges, and custom sections intact. Only refresh auto-detectable
  sections (commands, structure, versions).
- **Document your sources.** For each generated section, note which file(s) it
  was derived from. This makes the output verifiable and trustworthy.
- **Show diffs before overwriting.** When existing files will change significantly,
  show a summary of what changed (or a diff) and confirm with the user before writing.

---

## Workflow

### Step 0 — Zoom Out: Classify the Repository Archetype

Before gathering detailed context, observe the repository's top-level structure to
determine what *kind* of repo this is. This drives which signals to collect and which
template sections to populate.

#### Archetype signals

| Archetype | Key indicators |
|---|---|
| **`code`** | `package.json`, `Cargo.toml`, `pyproject.toml`, `*.sln`, `go.mod` at root |
| **`product`** | `docker-compose.yml`, `pnpm-workspace.yaml`, distinct frontend/backend apps, end-user focus |
| **`single-skill`**| `SKILL.md` at repository root; usually accompanied by `examples/` or `guidelines/` |
| **`multi-skills`**| `skills/` directory tree containing multiple nested `SKILL.md` files |
| **`courseware`** | `exercises/` directory; numbered folders like `XX.YY-name/`; domain CLI tools |
| **`docs`** | Primarily `.md` files, no build system; `gitbook.yaml`, `mkdocs.yml`, `_sidebar.md` |
| **`hybrid`** | Meaningful mix of two or more archetypes above |

#### Confidence evaluation

- **High confidence** (≥ 2 distinct signals point to the same archetype): state the
  archetype and proceed to Step 1.
- **Low confidence** (signals absent, conflicting, or unrecognised): **do not guess** —
  use the Forced Clarification path below.

#### Forced clarification (low-confidence path)

Ask **one targeted question** using the platform's interactive tool. Include the
specific signals observed and your best guess (if any).

**VS Code / Copilot** — use `vscode_askQuestions`:

```json
[{
  "header": "repo_archetype",
  "question": "I can't confidently classify this repository from its structure. What best describes it?",
  "message": "Signals observed: <list what you found>. My best guess: <archetype if any>.",
  "options": [
    { "label": "Code project (Node, Python, Rust, .NET, Go, etc.)" },
    { "label": "Product / App (End-user facing, full-stack, monorepo)" },
    { "label": "Single AI Skill (SKILL.md at root)" },
    { "label": "Multi-Skills Collection (skills/ directory)" },
    { "label": "Educational courseware (exercises, lessons)" },
    { "label": "Documentation site (Markdown, GitBook, MkDocs)" },
    { "label": "Hybrid — I'll describe below" }
  ],
  "allowFreeformInput": true
}]
```

**Claude Code / Gemini / other platforms** — ask the equivalent question directly
in the conversation, listing the same options. Wait for a reply before continuing.

After receiving the answer, re-evaluate. If resolved, continue to Step 1. If still
ambiguous, ask one targeted follow-up — then proceed with the best available
classification.

#### Output before continuing

State this block explicitly before moving to Step 1:

```
Archetype : <code | product | single-skill | multi-skills | courseware | docs | hybrid>
Confidence: <high | confirmed by user>
Signals   : <2–4 bullet observations>
```

---

### Step 1 — Gather Context & Delegate Execution

Once the archetype is confidently classified (and confirmed if required), **stop processing this SKILL.md** and delegate the rest of the workflow to the archetype-specific instruction file.

Use your native tools (e.g., `read_file`) to load the corresponding delegate file from the `delegates/` directory:

| Archetype | Delegate File to Load |
|---|---|
| `code`, `product`, `hybrid` | `delegates/repo-docs-code.md` |
| `single-skill`, `multi-skills` | `delegates/repo-docs-skills.md` |
| `docs`, `courseware` | `delegates/repo-docs-docs.md` |

**CRITICAL RULE:** Once you load the delegate file, follow **ITS** Step 1 through Step 6. The delegate file contains the highly-focused, noise-free rules for gathering context, restructuring, generating `README.md`/`AGENTS.md`, and final verification.

---

## Config file → field mapping

| Config file | Fields extracted |
|---|---|
| `package.json` | name, description, version, scripts, engines, license, dependencies |
| `pyproject.toml` / `setup.py` | name, version, python_requires, scripts/entry_points |
| `Cargo.toml` | name, version, description, edition |
| `go.mod` | module name, go version |
| `*.sln` / `*.csproj` | .NET project name, target framework, entry points |
| `Makefile` | targets used as commands |
| `.nvmrc` / `.node-version` | Node version requirement |
| `.python-version` | Python version requirement |
| `Dockerfile` | base image, exposed ports, run commands |
| `.github/workflows/*.yml` | CI commands, test commands |
| `jest.config.*` | test command, coverage config |
| `vitest.config.*` | test command |
| `ruff.toml` / `.ruff.toml` | lint command |
| `.eslintrc*` / `eslint.config.*` | lint command |
| `prettier.config.*` | format command |
| `turbo.json` | monorepo pipeline commands |
| `nx.json` | monorepo project structure |
| `pnpm-workspace.yaml` | monorepo packages |
| `compile.sh` / `setup.sh` / `build.sh` | custom build/setup commands |
| `.vscode/launch.json` | debug configurations |
| `CLAUDE.md` / `CONTRIBUTING.md` | tone, conventions, project context |
| `SKILL.md` (frontmatter) | skill name, description, trigger phrases |
| `skills/` directory | skills collection — categories, skill count |
| `exercises/XX.YY-*/` | courseware — section/exercise structure, numbering scheme |
| `gitbook.yaml` / `mkdocs.yml` / `_sidebar.md` | docs site — navigation, page tree |
| `CURSOR.md` / `AGENTS.md` (root) | AI agent conventions, architectural rules |

---

## Edge cases

**Monorepos**: Generate a root-level README/AGENTS.md that describes the workspace
and lists packages. Note individual packages may have their own docs.

**Private / no description**: Use directory name as project name; leave description
as `{{TODO: add a one-line project description}}`.

**Existing README with screenshots**: Preserve image links exactly — never remove
or rewrite media references.
