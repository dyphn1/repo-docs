#!/usr/bin/env python3
import json, sys, os
from pathlib import Path
import re

def guess_role(content, deps):
    content_lower = content.lower()
    if "spring-boot-starter-web" in content_lower: return "api-server/web"
    if "junit" in content_lower or "test" in content_lower: return "test-project"
    if "android" in content_lower: return "mobile-app"
    return "library/package"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ["target", "build", "node_modules", "bin"]]
        
        name = Path(dirpath).name
        deps = []
        is_java = False
        content = ""
        
        if "pom.xml" in filenames:
            is_java = True
            try:
                content = (Path(dirpath) / "pom.xml").read_text(encoding="utf-8")
                # Extract artifactId as name if available
                name_match = re.search(r'<artifactId>([^<]+)</artifactId>', content)
                if name_match: name = name_match.group(1)
                
                # Extract some dependencies
                matches = re.findall(r'<artifactId>([^<]+)</artifactId>', content)
                deps = [m for m in matches if m != name][:10]
            except: pass
            
        elif "build.gradle" in filenames or "build.gradle.kts" in filenames:
            is_java = True
            try:
                filename = "build.gradle" if "build.gradle" in filenames else "build.gradle.kts"
                content = (Path(dirpath) / filename).read_text(encoding="utf-8")
                
                # Extract dependencies
                matches = re.findall(r'(?:implementation|api|testImplementation)[\s\(]+[\'"]([^\'"]+)', content)
                deps = [m.split(':')[-1] if ':' in m else m for m in matches][:10]
            except: pass
            
        if is_java:
            workspaces.append({
                "workspace_name": name,
                "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                "primary_language": "Java/Kotlin",
                "role": guess_role(content, deps),
                "key_dependencies": deps[:10]
            })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
