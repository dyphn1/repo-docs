#!/usr/bin/env python3
import json, os, sys, re
from pathlib import Path
import yaml

def read_file_safe(path):
    try: return path.read_text(encoding="utf-8")
    except: return ""

def parse_yaml_frontmatter(content):
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match: return {}
    try:
        # Use pyyaml if available, else fallback to basic regex parsing
        try:
            import yaml as pyyaml
            return pyyaml.safe_load(match.group(1)) or {}
        except ImportError:
            frontmatter = {}
            for line in match.group(1).splitlines():
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip().strip("'\"")
            return frontmatter
    except: return {}

def extract_dependencies(content, all_skill_names):
    deps = set()
    content_lower = content.lower()
    for name in all_skill_names:
        # Check if another skill name is mentioned in the text (like /setup or setup-skill)
        if f"/{name}" in content_lower or f" {name} " in content_lower or f"`{name}`" in content_lower:
            deps.add(name)
    return list(deps)

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skill_files = list(root.rglob("SKILL.md"))
    
    archetype = "single-skill" if len(skill_files) == 1 and (root / "SKILL.md").exists() else "multi-skills"
    
    # First pass: get all skill names for dependency detection
    all_names = set()
    raw_skills = []
    
    for sf in skill_files:
        content = read_file_safe(sf)
        fm = parse_yaml_frontmatter(content)
        name = fm.get("name", sf.parent.name)
        if name: all_names.add(name)
        
        # Determine category (parent directory name)
        # If it's at root, category is 'root'
        category = "root"
        if len(sf.parts) > len(root.parts) + 1:
            # Usually skills/engineering/diagnose/SKILL.md -> category is 'engineering'
            # Find the parent of the folder containing SKILL.md
            parent_dir = sf.parent.parent.name
            if parent_dir != root.name and parent_dir != "skills":
                category = parent_dir
        
        # Look for supplementary resources
        resources = []
        for child in sf.parent.iterdir():
            if child.is_dir() and child.name in ["examples", "guidelines", "scripts", "docs"]:
                resources.append(child.name)
            elif child.is_file() and child.name not in ["SKILL.md", "README.md"]:
                resources.append(child.name)

        raw_skills.append({
            "path": str(sf.relative_to(root)),
            "name": name,
            "description": fm.get("description", ""),
            "category": category,
            "resources": resources,
            "content": content
        })

    # Second pass: detect dependencies and group
    categorized = {}
    for s in raw_skills:
        cat = s["category"]
        if cat not in categorized:
            categorized[cat] = []
        
        # Remove self from dependencies
        deps = extract_dependencies(s["content"], all_names)
        if s["name"] in deps: deps.remove(s["name"])
        
        categorized[cat].append({
            "name": s["name"],
            "path": s["path"],
            "description": s["description"],
            "dependencies": deps,
            "resources": s["resources"]
        })

    result = {
        "archetype_detected": archetype,
        "total_skills": len(skill_files),
        "categories": categorized
    }
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
