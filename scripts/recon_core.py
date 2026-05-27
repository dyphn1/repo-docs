#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "target"}

def should_ignore(name):
    return (name.startswith(".") and name not in {".nvmrc", ".node-version"}) or name in IGNORE

def build_tree(root, depth=2, current=0):
    if current >= depth: return []
    items = []
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except: return []
    for entry in entries:
        if should_ignore(entry.name): continue
        if entry.is_dir():
            items.append({"name": entry.name, "type": "dir", "children": build_tree(entry, depth, current + 1)})
        else:
            items.append({"name": entry.name, "type": "file"})
    return items

def detect_languages(root):
    ext_map = {
        ".ts": "TypeScript", ".js": "JavaScript", ".py": "Python", ".rs": "Rust", ".go": "Go",
        ".cs": "C#", ".fs": "F#", ".java": "Java", ".kt": "Kotlin",
        ".c": "C", ".cpp": "C++", ".h": "C/C++ Header", ".hpp": "C++ Header"
    }
    counts = {}
    
    # Using os.walk instead of rglob to properly skip ignored directories
    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out ignored directories in-place so os.walk doesn't traverse them
        dirnames[:] = [d for d in dirnames if not should_ignore(d)]
        
        for f in filenames:
            ext = os.path.splitext(f)[1]
            lang = ext_map.get(ext)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1
                
    return sorted(counts, key=lambda l: -counts[l])

def detect_package_manager(root):
    if (root / "pnpm-workspace.yaml").exists() or (root / "pnpm-lock.yaml").exists(): return "pnpm"
    if (root / "yarn.lock").exists(): return "yarn"
    if (root / "package-lock.json").exists(): return "npm"
    if (root / "Cargo.toml").exists(): return "cargo"
    if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists(): return "poetry/pip"
    if (root / "pom.xml").exists(): return "maven"
    if (root / "build.gradle").exists() or (root / "build.gradle.kts").exists(): return "gradle"
    if (root / "go.mod").exists(): return "go modules"
    if list(root.glob("*.sln")): return "msbuild/nuget"
    return "unknown"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    
    is_monorepo = any([
        (root / "pnpm-workspace.yaml").exists(),
        (root / "lerna.json").exists(),
        (root / "turbo.json").exists(),
        (root / "go.work").exists(),
        bool(list(root.glob("*.sln")))  # C# solution files often imply multiple projects
    ])
    
    result = {
        "repo_root": str(root),
        "project_name": root.name,
        "languages": detect_languages(root),
        "package_manager": detect_package_manager(root),
        "is_monorepo": is_monorepo,
        "tree_shallow": build_tree(root, depth=2)
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
