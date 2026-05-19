#!/usr/bin/env python3
import json, os, sys, re
from pathlib import Path

def read_json(path):
    try:
        return json.loads(path.read_text())
    except:
        return {}

def read_ci_commands(root):
    ci_dir = root / ".github/workflows"
    cmds = []
    if ci_dir.exists():
        for yml in ci_dir.glob("*.yml"):
            try:
                content = yml.read_text()
                matches = re.findall(r"run:\s*\|?\s*(.+)", content)
                cmds.extend([m.strip() for m in matches if m.strip()])
            except: pass
    return cmds[:20]

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    pkg = read_json(root / "package.json")
    
    result = {
        "scripts": pkg.get("scripts", {}),
        "dependencies": list(pkg.get("dependencies", {}).keys())[:15],
        "devDependencies": list(pkg.get("devDependencies", {}).keys())[:15],
        "ci_commands": read_ci_commands(root)
    }
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
