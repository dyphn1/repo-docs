#!/usr/bin/env python3
import json, os, sys, re
from pathlib import Path

def read_file_safe(path, max_bytes=2000):
    try: return path.read_text(encoding="utf-8")[:max_bytes]
    except: return ""

def scan_markdown_dirs(root):
    """Find directories containing primarily markdown files and group them."""
    md_dirs = {}
    
    # We'll scan depth 1 and 2 to find thematic folders
    for dirpath, dirnames, filenames in os.walk(root):
        rel_path = Path(dirpath).relative_to(root)
        if len(rel_path.parts) > 2 or rel_path.name.startswith('.') or rel_path.name in ["node_modules", "scripts"]:
            continue
            
        md_files = [f for f in filenames if f.endswith('.md')]
        if len(md_files) > 0:
            md_dirs[str(rel_path)] = {
                "count": len(md_files),
                "files_sample": md_files[:5]
            }
    
    return md_dirs

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    features = {
        "has_learning_path": False,
        "is_agentic_workspace": False,
        "has_task_tracking": False,
    }
    
    evidence = {
        "learning_path_files": [],
        "agent_files": [],
        "task_files": []
    }

    # 1. Learning Path Engine
    path_keywords = ["roadmap", "study", "guide", "start", "tutorial", "index"]
    for f in root.glob("*.md"):
        if any(k in f.name.lower() for k in path_keywords) and f.name.lower() != "readme.md":
            features["has_learning_path"] = True
            evidence["learning_path_files"].append(f.name)

    # 2. Agentic Engine
    agent_indicators = ["AGENTS.md", "IDENTITY.md", "SOUL.md", "TOOLS.md", "HEARTBEAT.md"]
    for ind in agent_indicators:
        if (root / ind).exists():
            features["is_agentic_workspace"] = True
            evidence["agent_files"].append(ind)
            
    github_agents_dir = root / ".github" / "agents"
    if github_agents_dir.exists() and github_agents_dir.is_dir():
        features["is_agentic_workspace"] = True
        evidence["agent_files"].extend([f.name for f in github_agents_dir.glob("*.md")])

    # 3. Task & Status Engine
    status_files = ["STATUS.md", "backlog.json", "CHANGELOG.md"]
    for sf in status_files:
        if (root / sf).exists():
            features["has_task_tracking"] = True
            evidence["task_files"].append(sf)
            
    task_dirs = ["tasks", "weekly-challenges", "issues"]
    for td in task_dirs:
        if (root / td).exists() and (root / td).is_dir():
            features["has_task_tracking"] = True
            evidence["task_files"].append(f"{td}/")

    # 4. Knowledge Grouping Engine
    md_directories = scan_markdown_dirs(root)

    result = {
        "repo_root": str(root),
        "capabilities": [k for k, v in features.items() if v],
        "evidence": evidence,
        "knowledge_directories": md_directories
    }

    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
