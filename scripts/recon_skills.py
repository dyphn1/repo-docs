#!/usr/bin/env python3
import json, os, sys, re, subprocess
from pathlib import Path

def read_file_safe(path):
    try: return path.read_text(encoding="utf-8")
    except: return ""

def extract_raw_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    # Use Git to find files to respect .gitignore
    try:
        git_output = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
        skill_files = [root / p for p in git_output.splitlines() if Path(p).name == "SKILL.md"]
    except Exception:
        # Safe fallback for non-git environments
        IGNORE_DIRS = {'.git', '.svn', 'node_modules', 'dist', 'build', 'venv', '__pycache__'}
        skill_files = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            if "SKILL.md" in filenames:
                skill_files.append(Path(dirpath) / "SKILL.md")
    
    archetype = "single-skill" if len(skill_files) == 1 and (root / "SKILL.md").exists() else "multi-skills"
    
    raw_skills = []
    
    for sf in skill_files:
        content = read_file_safe(sf)
        raw_fm = extract_raw_frontmatter(content)
        
        # Very basic extraction for name, leave the rest for AI
        name = sf.parent.name
        name_match = re.search(r'^name:\s*(.+)$', raw_fm, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip().strip('\'"')

        category = "root"
        if len(sf.parts) > len(root.parts) + 1:
            parent_dir = sf.parent.parent.name
            if parent_dir != root.name and parent_dir != "skills":
                category = parent_dir
        
        resources = []
        for child in sf.parent.iterdir():
            if child.is_dir() and child.name in ["examples", "guidelines", "scripts", "docs"]:
                resources.append(child.name)
            elif child.is_file() and child.name not in ["SKILL.md", "README.md"]:
                resources.append(child.name)

        raw_skills.append({
            "path": str(sf.relative_to(root)),
            "name": name,
            "category": category,
            "resources": resources,
            "raw_frontmatter": raw_fm,
            "content": content
        })

    result = {
        "archetype_detected": archetype,
        "total_skills": len(raw_skills),
        "skills_raw_data": raw_skills
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
