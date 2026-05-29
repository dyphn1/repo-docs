#!/usr/bin/env python3
import json, os, sys, re, subprocess
from pathlib import Path

def scan_markdown_dirs(root):
    md_dirs = {}
    
    # Attempt to use git ls-files as the source of truth
    try:
        git_output = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
        all_files = [Path(p) for p in git_output.splitlines()]
    except Exception:
        # Fallback to safe recursive scan if not a git repo
        IGNORE_DIRS = {'.git', '.svn', 'node_modules', 'dist', 'build', 'venv', '__pycache__'}
        all_files = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            all_files.extend([Path(dirpath) / f for f in filenames])
        
    for p in all_files:
        if p.suffix == '.md':
            parent_dir = str(p.parent)
            if parent_dir == ".":
                continue
                
            if parent_dir not in md_dirs:
                md_dirs[parent_dir] = {"count": 0, "files_sample": []}
                
            md_dirs[parent_dir]["count"] += 1
            if len(md_dirs[parent_dir]["files_sample"]) < 5:
                md_dirs[parent_dir]["files_sample"].append(p.name)
                
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
