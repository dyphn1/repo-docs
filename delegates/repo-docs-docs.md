# Repo Docs: Docs & Courseware Delegate

This delegate handles the `docs` and `courseware` archetypes.

## Step 1 — Gather repo context

1. **Deep Document Recon**:
   Run the specialized feature-driven document scanner:
   ```bash
   python /path/to/skill/scripts/recon_docs.py <repo_root>
   ```
   This script detects specific capabilities (`has_learning_path`, `is_agentic_workspace`, `has_task_tracking`) and groups markdown files semantically.

2. **Map the Courseware/Doc Tree**:
   If courseware, inspect the `exercises/` (or equivalent) directory. Identify section numbers, exercise variants (`problem/`, `solution/`), and extract titles from subfolder readmes.
   If docs, read `gitbook.yaml`, `mkdocs.yml`, or `_sidebar.md` to understand the navigation tree.

3. **AI Semantic Intervention**:
   Massive Monolithic Files: If `README.md` contains deep instructional prose or tutorials, **you MUST read it manually** and preserve it. Do not treat it as a simple index.

## Step 2 — Smart Restructure

- **Preserve Human Content (CRITICAL)**: Docs and Courseware are 90% human prose. You MUST preserve these sections entirely. Map them into the `{{PRESERVED_HUMAN_CONTENT}}` block.
- **Move to AGENTS.md**: Content authoring rules, domain lint commands, or strict formatting conventions (e.g., "all exercises must have a problem and solution folder").

## Step 3 — Generate README.md (For Humans)

Use `references/knowledge-readme-template.md`.

**Required Sections:**
- **Title & Summary**: Site or Course name + description
- **Overview & Learning Objectives**: 2–4 sentences on purpose.
- **Table of Contents / Course Outline**: Structured table or tree mapping the sections, chapters, or exercises.
- **How to Use**: Guidelines for the reader or student.
- **Preserved Human Content**: The core prose, tutorials, or deep dives.

*Note: Build, test, and packaging are completely omitted for pure docs.*

## Step 4 — Generate AGENTS.md (For AI)

**Required Sections:**
- **Overview**: The domain of this knowledge base.
- **Structure Conventions**:
  - Courseware: Document the section/exercise numbering scheme and folder conventions (e.g., `XX.YY-dash-case`, required `readme.md` in each subfolder).
  - Docs: The navigation update rules (e.g., "When adding a file, also update `_sidebar.md`").
- **Domain Tools**: Domain lint commands if any (e.g., `pnpm ai-hero-cli internal lint`).
- **Content Authoring Rules**: Tone, voice, formatting (e.g., "Use American English, prefer active voice").

## Step 5 — Write files & Verify

- Write to `<repo_root>/README.md` and `<repo_root>/AGENTS.md`.
- Ensure the Table of Contents matches the actual markdown files on disk.
- Ensure no human prose was accidentally deleted.

## Step 6 — Deliverables

- Output a Changelog paragraph.
- Output an Audit log.
