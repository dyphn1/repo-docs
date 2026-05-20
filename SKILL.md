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

### Step 1 — Gather repo context

Context gathering is archetype-specific. Use the branch that matches the archetype
identified in Step 0.

#### `code` — Run the core recon scripts

First, establish the baseline:
```bash
python /path/to/skill/scripts/recon_core.py <repo_root>
```

Then, extract execution context (scripts, CI, test frameworks):
```bash
python /path/to/skill/scripts/recon_code.py <repo_root>
```

> **If no scripts available**, run the recon steps manually — see
> `references/manual-recon.md`.

#### `product` — Deep Semantic & Workspace Recon

A product requires deep understanding of its boundaries and user documentation.

1. **Establish Baseline & Code Context**:
   Run `recon_core.py` and `recon_code.py` as shown in the `code` branch.
2. **Locate & Extract Documentation**:
   Run the docs semantic scanner to extract Getting Started guides and concepts:
   ```bash
   python /path/to/skill/scripts/recon_docs.py <repo_root>
   ```
3. **Map the Workspace Boundaries**:
   Analyze `apps/`, `packages/`, or `lib/` to map out the monorepo structure:
   ```bash
   python /path/to/skill/scripts/recon_workspace.py <repo_root>
   ```

#### `single-skill` and `multi-skills` — Run the skills recon script

Run the specialized skill parser:
```bash
python /path/to/skill/scripts/recon_skills.py <repo_root>
```

This script extracts YAML frontmatter, identifies categories (for `multi-skills`), spots supplementary folders (`examples/`, `guidelines/`), and detects cross-skill dependencies (e.g., when a skill mentions `/setup-project` in its text). Use this output to populate workflow dependencies and categorized tables.

Also read the root `README.md`, `CONTEXT.md`, `CLAUDE.md` (if any).

#### `courseware` — Map the exercise tree

Inspect the `exercises/` (or equivalent) directory. For each section and exercise:
- Section number and name (from directory prefix, e.g., `01-retrieval-skill-building`)
- Exercise variants present (`problem/`, `solution/`, `explainer/`)
- Title from the subfolder's `readme.md` first heading

Identify any domain lint tool from `package.json` scripts
(e.g., `pnpm ai-hero-cli internal lint`).

#### `docs` and `courseware` — Deep Document Recon

Run the specialized feature-driven document scanner:
```bash
python /path/to/skill/scripts/recon_docs.py <repo_root>
```
This script detects specific capabilities (`has_learning_path`, `is_agentic_workspace`, `has_task_tracking`) and groups markdown files semantically rather than providing a raw file tree.

#### `hybrid` — Combine applicable branches

Apply all relevant branches above in parallel, then merge the gathered context.

---

### Step 1.5 — AI Semantic Intervention (Dynamic Adjustment)

Python scripts cannot predict every custom repository structure. You **MUST** review the output from the recon scripts and actively intervene using your file-reading tools if necessary:

1. **Massive Monolithic Files**: If you detect that the existing `README.md` is unusually large or acts as a "Single-Page Book" (containing deep instructional prose, tutorials, or extensive sections), you MUST read it manually. **Do not treat it as a simple index.**
2. **Unrecognized Structures**: If the recon script returns unclassified folders with significant content (e.g., `solutions/`, `Materials/`), sample 1-2 files inside them manually to deduce the project's specific naming or structural conventions.
3. **Adaptation**: Use your findings to dynamically adapt the documentation strategy in Step 2. Do not be blindly constrained by the rigid output of the python script if it missed the semantic purpose of a folder.

---

**Always also read** any existing style-reference files (`CLAUDE.md`, `CONTRIBUTING.md`,
another README) to capture the project's tone, terminology, and formatting conventions.

---

### Step 2 — Smart Restructure & Migration (Scope & Merge)

Check which files already exist and analyze their current content. Rather than
blindly appending new information, actively restructure the existing documentation:

1. **Analyze Existing Sections**: Read the current `README.md` and `AGENTS.md` (if any).
2. **Force Audience Separation (Forking)**:
   - **Move to AGENTS.md**: Extract any sections from README related to "How to build from source", local dev server commands, testing, compilation, debugging, or coding conventions. Remove them from README entirely.
   - **Move to README.md**: Extract user-centric sections (Value Proposition, End-user Quick Start, Feature Tutorials, FAQ) from other files and consolidate them into the README.
3. **Content Preservation Engine (CRITICAL)**: If the existing `README.md` contains long-form instructional prose, domain-specific deep dives, or tutorials (common in `docs` and `courseware`), **you MUST preserve these sections entirely**. Do not delete them. Map them into the `{{PRESERVED_HUMAN_CONTENT}}` block of the new template.
4. **Enforce Strict Ordering**: Map all retained content to the exact section order prescribed by the templates in `references/` (e.g., Overview -> Getting Started -> Features -> Preserved Content). Do not leave legacy sections floating at the bottom.

| Situation | Action |
|---|---|
| Neither exists | Generate both from scratch using strict template order |
| README exists, AGENTS missing | Generate AGENTS.md; aggressively migrate dev instructions out of README |
| AGENTS exists, README missing | Generate README.md; ensure it is strictly user-focused |
| Both exist | Update both, migrating misplaced sections and enforcing template order |

**Always ask before overwriting** custom sections (badges, screenshots, license
blocks). If a major reorganization is needed, explain why and present a suggested outline
before proceeding.

---

### Step 3 — Generate README.md

Target audience: **human developers** visiting the repo.

Use the template in `references/readme-template.md` (or `references/product-readme-template.md` for products) as your structural guide. The
template includes **archetype-specific section sets** — use the set that matches the
archetype from Step 0, not all sections unconditionally.

#### Required sections (code archetype)

| Section | Description |
|---|---|
| **Title & Summary** | Project name + one-line description |
| **Badges / Quick Start** | Language, license, CI; setup + build in 3–5 steps |
| **Table of Contents** | Auto-generated |
| **Overview & Goals** | 2–4 sentences on purpose and context |
| **Architecture & Components** | High-level module list |
| **Project Structure** | Abbreviated tree with one-line dir descriptions |
| **System Requirements** | OS, runtime versions (Node, Python, .NET, etc.) |
| **Installation / Setup** | Exact commands to prepare the environment |
| **Build** | Per-language build commands |
| **Usage** | Primary usage commands or code snippet |
| **Test** | How to run tests (full suite + single file) |
| **Debugging** | Reference `.vscode/launch.json` or equivalent if present |
| **Packaging & Release** | How to produce artifacts (VSIX, wheel, binary, etc.) |
| **Contributing** | Brief note or link to CONTRIBUTING.md |
| **Troubleshooting / FAQ** | Common pitfalls found in the codebase |
| **License** | SPDX ID from LICENSE file or package.json |
| **For AI Agents** | One-line notice pointing agents to `AGENTS.md` (see below) |

Skip sections gracefully when the required info is genuinely unavailable; use
`{{TODO: ...}}` with a verification hint rather than omitting silently.

Write in **clear, friendly prose**. Avoid bullet overload — use bullets only for
lists of commands or options. Preserve project-specific terminology exactly as
found in the source files.

#### AI agent notice in README

Always include a short notice near the top of README.md (after the one-line
description, before the Table of Contents) to help AI models that do not
automatically read `AGENTS.md`:

```markdown
> **AI agents:** Read [`AGENTS.md`](AGENTS.md) for architecture, exact commands,
> conventions, and constraints before making changes.
```

This ensures older or less-capable models — which may only read `README.md` —
still get directed to the authoritative machine-readable context.

**Content segregation rule:** Any content primarily useful to an AI agent
(exact commands, architecture details, coding conventions, constraints,
gotchas) belongs in `AGENTS.md`, **not** in `README.md`. If such content
currently exists in README.md, move it to AGENTS.md and replace it with a
one-line pointer. Human-facing prose (overview, screenshots, contributing
guide, license) stays in README.md.

#### Multi-language projects

When a repo mixes languages (e.g., C# + TypeScript, Python + Rust), include
**separate Quick Start and Build sub-sections** for each toolchain. Label them
clearly (e.g., "Build — TypeScript", "Build — .NET").

---

### Step 4 — Generate AGENTS.md

Target audience: **AI coding agents** (Claude Code, Copilot, etc.).

Use `references/agents-template.md` (or `references/product-agents-template.md` for products, `references/knowledge-agents-template.md` for docs/courseware) as your baseline.

Use the template in `references/agents-template.md` as your structural guide. For
non-`code` archetypes, replace the **Commands** block with **Workflows & Commands**
and populate archetype-specific sections as described in the template.

#### Migrate AI-specific content from README

Before generating AGENTS.md from scratch, scan the existing README.md for any
content that belongs in AGENTS.md instead:
- Sections titled "For AI", "Agent notes", "CLAUDE notes", "Copilot context", etc.
- Detailed command tables intended for automation
- Architecture diagrams described in text form
- Constraint or gotcha lists

Move that content into AGENTS.md verbatim (preserving intent), then replace it
in README.md with the standard AI agent notice (see Step 3).

Must include:
- **Project overview** — one tight paragraph (what it is, main tech stack)
- **Commands** — exact, copy-pasteable commands for:
  - `install` / `setup`
  - `dev` / `run`
  - `test` (including how to run a single test file)
  - `lint` / `format`
  - `build`
- **Architecture** — key directories and what lives in each (no fluff)
- **Conventions** — coding style, naming patterns, import conventions detected
  from the codebase or config files (eslint, prettier, ruff, etc.)
- **Important constraints** — files/dirs NOT to edit (generated code, lock files,
  vendor dirs), env vars required, secrets handling
- **Common gotchas** — patterns found that could trip up an AI (e.g., monorepo
  setup, custom aliases, non-standard test runner config)

Write in **terse, directive style** — imperative sentences, no filler. This file
is machine-read first.

---

### Step 5 — Write files

Write to `<repo_root>/README.md` and `<repo_root>/AGENTS.md`.

If updating existing files, show a diff summary of what changed before writing.
Always confirm with the user before overwriting.

---

### Step 6 — Verify

Run the following checklist before declaring done:

- [ ] Every command in README.md and AGENTS.md exists in a config file or is a
      well-known standard tool invocation.
- [ ] Version numbers (Node, Python, .NET, etc.) match what's in config files.
- [ ] No `[Your Name]`, `TODO` (without `{{}}`), or other stale placeholder text.
- [ ] All `{{TODO: ...}}` entries include a clear description of what's missing
      and how to verify it.
- [ ] Media/screenshot links from the original README are preserved exactly.
- [ ] Multi-language repos have separate command sections per toolchain.
- [ ] README.md contains the AI agent notice pointing to `AGENTS.md`.
- [ ] No AI-specific content (commands, constraints, gotchas) remains in README.md
      without a corresponding entry in AGENTS.md.

Report remaining `{{TODO}}` gaps to the user with actionable next steps.

---

### Step 7 — Produce deliverables

After writing the files, output:

1. **Changelog paragraph** — a short PR/commit body describing what was updated,
   added, or removed compared to the previous version.
2. **Audit log** — list every file that was read during recon, with an ISO 8601
   timestamp of when analysis was performed.

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

**Multiple languages**: List all detected languages; include separate Quick Start
and command sections per toolchain.

**Private / no description**: Use directory name as project name; leave description
as `{{TODO: add a one-line project description}}`.

**Existing README with screenshots**: Preserve image links exactly — never remove
or rewrite media references.

**Custom scripts** (e.g., `compile.sh`, `setup.sh`): Include their path and a
one-line summary of what they do (inferred from script header or first few lines).
Mark behavior that can't be confirmed with `{{TODO: verify <script> behavior}}`.

**AI Skills repos**: List every skill (`name` + `description`) in a Skills Index
table in README. README should explain how to activate skills in an AI assistant.
AGENTS.md should describe authoring conventions: frontmatter schema, trigger phrases,
file placement, and naming rules.

**Courseware repos**: Document the section/exercise numbering scheme and folder
conventions. README should list the full course outline as a structured table or tree.
AGENTS.md should include the domain lint command, required file structure, and naming
rules (e.g., `XX.YY-dash-case`, required `readme.md` in each variant subfolder).

**Documentation sites**: Treat `.md` file titles as the structural skeleton. README
should summarise the site's purpose and link to the live URL if known. AGENTS.md should
note the build/publish workflow and any content authoring rules.
