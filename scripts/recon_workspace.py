#!/usr/bin/env python3
import json, os, sys, subprocess
from pathlib import Path

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    scripts_dir = Path(__file__).parent
    
    analyzers = [f for f in scripts_dir.iterdir() if f.name.startswith("analyze_") and f.name.endswith(".py")]
    
    all_workspaces = []
    
    for analyzer in analyzers:
        try:
            result = subprocess.run([sys.executable, str(analyzer), str(root)], capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            if isinstance(data, list):
                all_workspaces.extend(data)
        except Exception as e:
            # Fail-fast for individual analyzer, but let others continue
            print(f"Error running {analyzer.name}: {e}", file=sys.stderr)
            
    # Calculate unrecognized directories at top level
    recognized_paths = {Path(ws["path"]).resolve() for ws in all_workspaces}
    
    # Use git ls-files if available, fallback to basic scan
    try:
        git_output = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
        tracked_files = [root / p for p in git_output.splitlines()]
        # Extract unique top-level directories from tracked files
        top_level_dirs = {p.parts[len(root.parts)] for p in tracked_files if len(p.parts) > len(root.parts) and (root / p.parts[len(root.parts)]).is_dir()}
        top_level_dirs = [root / d for d in top_level_dirs]
    except Exception:
        # Fallback if not a git repo
        IGNORE_DIRS = {'.git', '.svn', 'node_modules', 'dist', 'build', 'venv', '__pycache__'}
        top_level_dirs = [d for d in root.iterdir() if d.is_dir() and d.name not in IGNORE_DIRS]
    
    unrecognized = []
    for d in top_level_dirs:
        # A directory is recognized if it IS a workspace path or if it CONTAINS a workspace path
        is_recognized = any(d == rp or d in rp.parents for rp in recognized_paths)
        if not is_recognized:
            unrecognized.append(d.name)
            
    summary = {
        "total_top_level_directories": len(top_level_dirs),
        "recognized_count": len(top_level_dirs) - len(unrecognized),
        "unrecognized_directories": sorted(unrecognized)
    }
            
    print(json.dumps({"summary": summary, "workspaces": all_workspaces}, indent=2))

if __name__ == "__main__": main()
