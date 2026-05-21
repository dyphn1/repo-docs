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
            
    print(json.dumps({"workspaces": all_workspaces}, indent=2))

if __name__ == "__main__": main()
