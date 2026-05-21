#!/usr/bin/env python3
import json, sys, os
from pathlib import Path

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != "target"]
        
        if "Cargo.toml" in filenames:
            name = Path(dirpath).name
            deps = []
            try:
                content = (Path(dirpath) / "Cargo.toml").read_text(encoding="utf-8")
                in_deps = False
                for line in content.splitlines():
                    if line.startswith("name = "): name = line.split("=")[1].strip().strip('\'"')
                    elif line.startswith("[dependencies]"): in_deps = True
                    elif line.startswith("["): in_deps = False
                    elif in_deps and "=" in line: deps.append(line.split("=")[0].strip())
            except: pass
            
            role = "api-server" if any(d in ["actix-web", "axum", "tokio"] for d in deps) else "library/binary"
            
            workspaces.append({
                "workspace_name": name,
                "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                "primary_language": "Rust",
                "role": role,
                "key_dependencies": deps[:10]
            })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
