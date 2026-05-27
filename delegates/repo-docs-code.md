# Repo Docs: Code / Product / Hybrid Delegate

This delegate handles the `code`, `product`, and `hybrid` archetypes.

## Operating Scope (Single vs. Multi-Repo)
- **Single Target**: If documenting a single repository or directory, execute the workflow for that target.
- **Monorepo / Multi-Module Strategy (Bottom-Up Context)**: Do NOT attempt to read all source code or configurations of submodules from the root. This causes severe attention degradation. Instead:
  1. Document the root repository by examining its top-level config.
  2. To understand what is inside the submodules, **read the `README.md` and `AGENTS.md` of those submodules if they exist**.
  3. Let the already-processed sub-documents feed your root summary. Do not reinvent the wheel.

## Step 1 — Collect (Gather Context)

1. **Establish Baseline & Code Context**:
   Run the core recon script:
   ```bash
   python /path/to/skill/scripts/recon_workspace.py <target_dir>
   ```
   *Fallback Mechanism*: If the python script fails, use your native tools (`file_search`, `read_file`) to inspect `package.json`, `Cargo.toml`, `pyproject.toml`, `*.sln`, etc.

2. **Semantic Intervention**:
   Review the output. If the project contains custom orchestrator scripts (e.g., `compile.sh`, `setup.bat`), read their first 20 lines to understand their parameters.
   If massive monolithic `README.md` files exist, read them to extract `{{PRESERVED_HUMAN_CONTENT}}`.

## Step 2 — Think & Correlate (The "Aha!" Moment)

**CRITICAL:** Before generating any markdown files, you MUST output a `<Thinking>` block to correlate the collected data and deduce the true nature of the project. Do not act blindly.
- **Analyze the Stack**: E.g., "I see C# (.csproj) and TypeScript (package.json). This is a hybrid app. C# is likely the backend."
- **Analyze the Target Platforms**: E.g., "The C# project has `<RuntimeIdentifier>win-x64</RuntimeIdentifier>` and `<TargetFramework>net472</TargetFramework>`, meaning it's a Windows desktop or legacy server app."
- **Structure Strategy**: E.g., "Because it's a hybrid, I should split the Build instructions into a Frontend section and a Backend section."

## Step 3 — Smart Restructure & Migration

- **Move to AGENTS.md**: Extract sections related to "How to build from source", local dev commands, testing, compilation, debugging, or coding conventions.
- **Move to README.md**: Extract user-centric sections (Value Proposition, End-user Quick Start, Feature Tutorials, FAQ).
- **Preserve Human Content**: Deep dives or domain tutorials MUST be preserved and injected into the `{{PRESERVED_HUMAN_CONTENT}}` block.

## Step 4 — Generate README.md (For Humans)

Use `references/product-readme-template.md` or `references/readme-template.md`.

**Required Sections (Must be present; if info is missing, log it for the Action Required block):**
- **Title & Summary**: Project name + one-line description
- **Overview & Goals**: 2–4 sentences on purpose and context
- **System Requirements**: OS, minimum runtime versions (Node, Python, .NET, etc.).
- **Installation / Setup**: Exact commands to prepare the environment
- **Build & Usage**: Primary usage commands, separated by language if hybrid
- **For AI Agents**: "Read `AGENTS.md` for architecture, exact commands, conventions, and constraints before making changes."

**Conditional / Optional Sections (Include if relevant/detected, otherwise omit silently):**
- **Badges / Quick Start**: Setup + build in 3–5 steps
- **Table of Contents**: Auto-generated
- **Core Modules & Submodules Matrix**: High-level module list (Name, Language, Path, Role) with Markdown links to each submodule's specific `README.md` and `AGENTS.md` (if available) for quick navigation. **CRITICAL: You must list ALL detected submodules exhaustively. Do not truncate, abbreviate, or skip items even if the list is long.**
- **Project Structure**: Abbreviated tree with one-line dir descriptions
- **Test**: How to run tests
- **Debugging**: Highlight `.vscode/launch.json` or `tasks.json` if present
- **Packaging & Release**: How to produce artifacts
- **AI Skills Index**: List available `.agents/` or `.github/agents/` tools if present
- **Contributing / FAQ / License**: As applicable

*Rule: Do NOT generate `{{TODO: ...}}` placeholders in the text. For missing **Required Sections**, omit them from the main body but append a single `## ⚠️ Action Required` section at the very bottom of the document listing what the human needs to provide.*

## Step 5 — Generate AGENTS.md (For AI)

**README is strictly for human consumption. AGENTS is strictly for AI consumption.**

**Required Sections (Must be present; if missing, log for Action Required block):**
- **Project overview**: one tight paragraph (what it is, main tech stack)
- **Toolchain Strict Constraints**: Package managers (e.g., MUST use `pnpm`), minimum runtimes.
- **Commands & Orchestrators**:
  - `install` / `setup`, `dev` / `run`, `test`, `lint`, `build`
  *Note on Build Scripts: Prioritize custom shell/bat scripts (e.g., `compile.sh`) over native ecosystem commands if their purpose is clear.*
- **Architecture**: key directories and what lives in each
- **Conventions & Constraints**: coding style, files NOT to edit (generated code, lock files)

**Conditional / Optional Sections (Include if relevant, else omit):**
- **Submodule Navigation Map**: Direct link mapping to respective `AGENTS.md` or `README.md` files of submodules/packages.
- **Boundary & Override Rules**: State rules on what directories AI should NOT cross-contaminate (e.g., "Frontend code must not edit Backend source directly").
- **Debugging Paths**: Document existing `.vscode/launch.json` or `tasks.json` execution paths. Do NOT create or invent new debug files for the user.

*Rule: As with README, use a `## ⚠️ Action Required` block at the bottom for missing required info instead of inline TODOs.*

## Step 6 — Write files & Verify

- Write to `<target_dir>/README.md` and `<target_dir>/AGENTS.md`.
- Ensure all commands exist in config files or scripts.
- Ensure no AI-specific content remains in README.md.
- Ensure version numbers match config files.

## Step 7 — Deliverables

- Output a Changelog paragraph.
- Output an Audit log.
