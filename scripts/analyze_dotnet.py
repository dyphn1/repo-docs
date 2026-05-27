#!/usr/bin/env python3
import json, sys, os
from pathlib import Path
import re

def guess_role(content, dir_name):
    content_lower = content.lower()
    if "microsoft.net.sdk.web" in content_lower: return "api-server/web"
    if "xunit" in content_lower or "nunit" in content_lower or "mstest" in content_lower: return "test-project"
    if "avalonia" in content_lower or "wpf" in content_lower or "windows.forms" in content_lower: return "desktop-app"
    return "library/package"

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    workspaces = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        # Ignore hidden directories and common output directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ["bin", "obj", "packages", "TestResults"]]
        
        for file in filenames:
            if file.endswith(".csproj") or file.endswith(".fsproj"):
                name = file[:-7]
                deps = []
                role = "library/package"
                target_framework = "unknown"
                runtime_identifiers = []
                try:
                    content = (Path(dirpath) / file).read_text(encoding="utf-8")
                    
                    # Extract TargetFramework
                    tf_match = re.search(r'<TargetFramework>(.*?)</TargetFramework>', content, re.IGNORECASE)
                    tfs_match = re.search(r'<TargetFrameworks>(.*?)</TargetFrameworks>', content, re.IGNORECASE)
                    if tf_match: target_framework = tf_match.group(1)
                    elif tfs_match: target_framework = tfs_match.group(1)
                    
                    # Extract RuntimeIdentifier(s)
                    rid_match = re.search(r'<RuntimeIdentifier>(.*?)</RuntimeIdentifier>', content, re.IGNORECASE)
                    rids_match = re.search(r'<RuntimeIdentifiers>(.*?)</RuntimeIdentifiers>', content, re.IGNORECASE)
                    if rid_match: runtime_identifiers = [rid_match.group(1)]
                    elif rids_match: runtime_identifiers = [r.strip() for r in rids_match.group(1).split(';') if r.strip()]
                    
                    # Extract PackageReferences
                    # e.g., <PackageReference Include="Newtonsoft.Json" Version="13.0.1" />
                    matches = re.findall(r'<PackageReference\s+Include="([^"]+)"', content, re.IGNORECASE)
                    deps = list(matches)
                    
                    role = guess_role(content, Path(dirpath).name)
                except: pass
                
                workspaces.append({
                    "workspace_name": name,
                    "path": str(Path(dirpath).relative_to(root)) if dirpath != str(root) else ".",
                    "primary_language": "C#/.NET" if file.endswith(".csproj") else "F#/.NET",
                    "role": role,
                    "target_framework": target_framework,
                    "runtime_identifiers": runtime_identifiers,
                    "key_dependencies": deps[:10]
                })

    print(json.dumps(workspaces, indent=2))

if __name__ == "__main__": main()
