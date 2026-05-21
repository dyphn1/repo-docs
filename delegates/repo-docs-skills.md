# Repo Docs: Skills Delegate

This delegate handles the `single-skill` and `multi-skills` archetypes.

## Step 1 — Gather repo context

1. **Run the skills recon script**:
   ```bash
   python /path/to/skill/scripts/recon_skills.py <repo_root>
   ```
   This script extracts YAML frontmatter, identifies categories, spots supplementary folders (`examples/`, `guidelines/`), and extracts raw content.

2. **AI Semantic Intervention**:
   Analyze the raw frontmatter and content returned by the script. Deduce cross-skill dependencies (e.g., when a skill mentions `/setup-project` in its text). Use this analysis to populate workflow dependencies and categorized tables.
   Also read the root `README.md`, `CONTEXT.md`, `CLAUDE.md` (if any) to preserve human-written documentation.

## Step 2 — Smart Restructure

- For skills, the `README.md` acts as a catalog.
- The `AGENTS.md` (or `.github/copilot-instructions.md`) dictates how AI agents should interact with these skills.
- Preserve any tutorial prose or custom examples in the `{{PRESERVED_HUMAN_CONTENT}}`.

## Step 3 — Generate README.md (For Humans)

Use `references/multi-skills-readme-template.md` or `single-skill-readme-template.md`.

**Required Sections:**
- **Title & Summary**: Library name + description
- **Overview**: What these skills are for.
- **Skills Catalog**: A table of all detected skills. Group by category if `multi-skills`. Include columns for: Name, Trigger Phrase, Description, and Dependencies.
- **Usage**: How a human user should activate these skills in their AI assistant.
- **Preserved Human Content**: Examples, best practices, etc.

*Note: Build, test, and system requirements are usually NOT required unless the skills require specific local tools (like python scripts).*

## Step 4 — Generate AGENTS.md (For AI)

**Required Sections:**
- **Overview**: Purpose of this skill library.
- **Authoring Conventions**: Rules for creating new skills in this repository.
  - Frontmatter schema (must include `name`, `description`).
  - File placement (`.agents/skills/<skill-name>/SKILL.md`).
- **Trigger Guidelines**: How AI agents should interpret user requests to invoke these skills.
- **Dependencies & Interoperability**: If certain skills must be called before others.

## Step 5 — Write files & Verify

- Write to `<repo_root>/README.md` and `<repo_root>/AGENTS.md`.
- Ensure every skill listed in the README actually exists in the directory tree.
- Ensure the frontmatter requirements in AGENTS.md match the real `.md` files.

## Step 6 — Deliverables

- Output a Changelog paragraph.
- Output an Audit log.
