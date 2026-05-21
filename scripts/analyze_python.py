#!/usr/bin/env python3
import json, sys, os
from pathlib import Path

def guess_role(deps, dir_name):
    deps_lower = [d.lower() for d in deps]
    if any("django" in d or "fastapi" in d or "flask" in d for d in deps_lower): return "api-server"
    if any("pandas" in d or "numpy" in d or "torch" in d for d in deps_lower): return "data-science/ml"
    return "library/package"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ["venv", "env", "__pycache__"]]
        
        deps = []
        is_python = False
        name = Path(dirpath).name
        
        if "pyproject.toml" in filenames:
            is_python = True
            try:
                content = (Path(dirpath) / "pyproject.toml").read_text(encoding="utf-8")
                # simple extraction
                for line in content.splitlines():
                    if line.startswith("name = "): name = line.split("=")[1].strip().strip('\'"')
            except: pass
        elif "requirements.txt" in filenames:
            is_python = True
            try:
                content = (Path(dirpath) / "requirements.txt").read_text(encoding="utf-8")
                deps = [line.split("==")[0].strip() for line in content.splitlines() if line and not line.startswith("#")]
            except: pass
            
        if is_python:
            workspaces.append({
                "workspace_name": name,
                "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                "primary_language": "Python",
                "role": guess_role(deps, name),
                "key_dependencies": deps[:10]
            })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
