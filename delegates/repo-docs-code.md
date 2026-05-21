# Repo Docs: Code / Product / Hybrid Delegate

This delegate handles the `code`, `product`, and `hybrid` archetypes.

## Step 1 — Gather repo context

1. **Establish Baseline & Code Context**:
   Run the core recon script:
   ```bash
   python /path/to/skill/scripts/recon_workspace.py <repo_root>
   ```
   *Fallback Mechanism*: If the python script fails, use your native tools (`file_search`, `read_file`) to inspect `package.json`, `Cargo.toml`, `pyproject.toml`, `*.sln`, etc.

2. **Semantic Intervention**:
   Review the output. If the project contains custom orchestrator scripts (e.g., `compile.sh`, `setup.bat`), read their first 20 lines to understand their parameters.
   If massive monolithic `README.md` files exist, read them to extract `{{PRESERVED_HUMAN_CONTENT}}`.

## Step 2 — Smart Restructure & Migration

- **Move to AGENTS.md**: Extract sections related to "How to build from source", local dev commands, testing, compilation, debugging, or coding conventions.
- **Move to README.md**: Extract user-centric sections (Value Proposition, End-user Quick Start, Feature Tutorials, FAQ).
- **Preserve Human Content**: Deep dives or domain tutorials MUST be preserved and injected into the `{{PRESERVED_HUMAN_CONTENT}}` block.

## Step 3 — Generate README.md (For Humans)

Use `references/product-readme-template.md` or `references/readme-template.md`.

**Required Sections:**
- **Title & Summary**: Project name + one-line description
- **Badges / Quick Start**: Setup + build in 3–5 steps
- **Table of Contents**: Auto-generated
- **Overview & Goals**: 2–4 sentences on purpose and context
- **Core Modules & Submodules Matrix**: High-level module list (Name, Language, Path, Role) with Markdown links to each submodule's specific `README.md` and `AGENTS.md` (if available) for quick navigation.
- **Project Structure**: Abbreviated tree with one-line dir descriptions
- **System Requirements**: OS, minimum runtime versions (Node, Python, .NET, etc.).
- **Installation / Setup**: Exact commands to prepare the environment
- **Build & Usage**: Primary usage commands, separated by language if hybrid
- **Test**: How to run tests
- **Debugging**: Highlight `.vscode/launch.json` or `tasks.json` if present
- **Packaging & Release**: How to produce artifacts
- **AI Skills Index**: List available `.agents/` or `.github/agents/` tools if present
- **Contributing / FAQ / License**: As applicable
- **For AI Agents**: "Read `AGENTS.md` for architecture, exact commands, conventions, and constraints before making changes."

*Rule: Skip optional sections gracefully. For core required sections (Build, Install, Core Modules), use `{{TODO: ...}}` instead of omitting silently.*

## Step 4 — Generate AGENTS.md (For AI)

**README is strictly for human consumption. AGENTS is strictly for AI consumption.**

**Required Sections:**
- **Project overview**: one tight paragraph (what it is, main tech stack)
- **Toolchain Strict Constraints**: Package managers (e.g., MUST use `pnpm`), minimum runtimes.
- **Submodule Navigation Map**: Direct link mapping to respective `AGENTS.md` or `README.md` files of submodules/packages.
- **Commands & Orchestrators**:
  - `install` / `setup`, `dev` / `run`, `test`, `lint`, `build`
  *Note on Build Scripts: Prioritize custom shell/bat scripts (e.g., `compile.sh`) over native ecosystem commands if their purpose is clear.*
- **Boundary & Override Rules**: State rules on what directories AI should NOT cross-contaminate (e.g., "Frontend code must not edit Backend source directly").
- **Architecture**: key directories and what lives in each
- **Conventions & Constraints**: coding style, files NOT to edit (generated code, lock files)
- **Debugging Paths**: Document existing `.vscode/launch.json` or `tasks.json` execution paths. Do NOT create or invent new debug files for the user.

## Step 5 — Write files & Verify

- Write to `<repo_root>/README.md` and `<repo_root>/AGENTS.md`.
- Ensure all commands exist in config files or scripts.
- Ensure no AI-specific content remains in README.md.
- Ensure version numbers match config files.

## Step 6 — Deliverables

- Output a Changelog paragraph.
- Output an Audit log.
