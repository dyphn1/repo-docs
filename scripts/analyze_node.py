#!/usr/bin/env python3
import json, sys, os
from pathlib import Path

def read_json(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except: return {}

def guess_role(pkg_json, dir_name):
    deps = list(pkg_json.get("dependencies", {}).keys()) + list(pkg_json.get("devDependencies", {}).keys())
    if "react" in deps or "vue" in deps or "next" in deps or "vite" in deps: return "frontend"
    if "express" in deps or "nestjs" in deps or "hono" in deps or "fastify" in deps: return "api-server"
    if "drizzle-orm" in deps or "prisma" in deps or "sequelize" in deps: return "database"
    if "docs" in dir_name or "spec" in dir_name: return "documentation"
    return "library/package"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    # Discover package.json files, ignoring hidden directories and node_modules
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != "node_modules"]
        if "package.json" in filenames:
            pkg_path = Path(dirpath) / "package.json"
            pkg = read_json(pkg_path)
            role = guess_role(pkg, Path(dirpath).name)
            workspaces.append({
                "workspace_name": pkg.get("name", Path(dirpath).name),
                "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                "primary_language": "TypeScript/JavaScript",
                "role": role,
                "key_dependencies": list(pkg.get("dependencies", {}).keys())[:10],
                "scripts": pkg.get("scripts", {}),
                "engines": pkg.get("engines", {})
            })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
