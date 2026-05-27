#!/usr/bin/env python3
import json, sys, os
from pathlib import Path

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ["vendor", "node_modules", "bin"]]
        
        if "go.mod" in filenames:
            name = Path(dirpath).name
            deps = []
            role = "api-server/binary" # Go is often backend
            try:
                content = (Path(dirpath) / "go.mod").read_text(encoding="utf-8")
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith("module "):
                        name = line.split(" ")[1].split("/")[-1]
                    elif not line.startswith("go ") and not line.startswith("require") and line:
                        parts = line.split()
                        if len(parts) >= 2 and "." in parts[0]:
                            # e.g., github.com/gin-gonic/gin v1.7.0 -> gin-gonic/gin
                            clean_dep = parts[0].replace('"', '')
                            deps.append(clean_dep.split('/')[-1])
            except: pass
            
            workspaces.append({
                "workspace_name": name,
                "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                "primary_language": "Go",
                "role": role,
                "key_dependencies": deps[:10]
            })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
