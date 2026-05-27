#!/usr/bin/env python3
import json, sys, os
from pathlib import Path
import re

def guess_role(content, file_name):
    content_lower = content.lower()
    if "executable" in content_lower or "add_executable" in content_lower or "application" in content_lower: return "application"
    return "library/binary"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ["build", "out", "bin", "obj", "node_modules"]]
        
        for file in filenames:
            if file == "CMakeLists.txt" or file.endswith(".vcxproj"):
                name = Path(dirpath).name
                if file.endswith(".vcxproj"):
                    name = file[:-8]
                    
                deps = []
                content = ""
                try:
                    content = (Path(dirpath) / file).read_text(encoding="utf-8")
                    
                    if file == "CMakeLists.txt":
                        # Attempt to extract project name
                        name_match = re.search(r'project\s*\(\s*([^ \)]+)', content, re.IGNORECASE)
                        if name_match: name = name_match.group(1)
                        
                        # Attempt to find linked libraries (target_link_libraries)
                        link_matches = re.findall(r'target_link_libraries\s*\(\s*[^ ]+\s+([^\)]+)\)', content, re.IGNORECASE)
                        for match in link_matches:
                            deps.extend([d for d in match.split() if d and not d.startswith('PRIVATE') and not d.startswith('PUBLIC')])
                            
                    elif file.endswith(".vcxproj"):
                        # Extract ProjectReference or AdditionalDependencies
                        ref_matches = re.findall(r'<ProjectReference Include="([^"]+)"', content)
                        deps.extend([Path(m).stem for m in ref_matches])
                except: pass
                
                # Avoid extreme duplication if multiple vcxproj exist in same dir with same name roughly
                # But it's okay for now.
                
                workspaces.append({
                    "workspace_name": name,
                    "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                    "primary_language": "C/C++",
                    "role": guess_role(content, file),
                    "key_dependencies": list(set(deps))[:10]
                })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
