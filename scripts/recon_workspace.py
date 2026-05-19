#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {}

def guess_role(pkg_json, dir_name):
    deps = list(pkg_json.get("dependencies", {}).keys()) + list(pkg_json.get("devDependencies", {}).keys())
    if "react" in deps or "vue" in deps or "next" in deps or "vite" in deps:
        return "frontend"
    if "express" in deps or "nestjs" in deps or "hono" in deps or "fastify" in deps:
        return "api-server"
    if "drizzle-orm" in deps or "prisma" in deps or "sequelize" in deps:
        return "database"
    if "docs" in dir_name or "spec" in dir_name:
        return "documentation"
    return "library/package"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for search_dir in ["apps", "packages", "lib", "artifacts"]:
        target = root / search_dir
        if not target.exists(): continue
        
        for child in target.iterdir():
            if not child.is_dir(): continue
            pkg_path = child / "package.json"
            if pkg_path.exists():
                pkg = read_json(pkg_path)
                role = guess_role(pkg, child.name)
                workspaces.append({
                    "name": pkg.get("name", child.name),
                    "path": str(child.relative_to(root)),
                    "inferred_role": role,
                    "description": pkg.get("description", "")
                })

    print(json.dumps({"workspaces": workspaces}, indent=2))

if __name__ == "__main__": main()
