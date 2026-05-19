#!/usr/bin/env python3
import json, os, sys, re
from pathlib import Path

def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    doc_dirs = ["docs", "wiki", "gitbook", "documentation"]
    found_docs = []
    
    for d in doc_dirs:
        target = root / d
        if not target.exists() or not target.is_dir(): continue
        
        for md_file in target.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                heading = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                title = heading.group(1) if heading else md_file.stem
                
                topics = []
                lower_content = content.lower()
                if "quick start" in lower_content or "getting started" in lower_content: topics.append("Getting Started")
                if "concept" in lower_content or "architecture" in lower_content: topics.append("Concepts/Architecture")
                if "faq" in lower_content or "troubleshoot" in lower_content: topics.append("FAQ")
                if "deploy" in lower_content or "install" in lower_content: topics.append("Deployment")
                
                if topics: # Only include if it contains semantic value for our templates
                    found_docs.append({
                        "file": str(md_file.relative_to(root)),
                        "title": title,
                        "topics": topics,
                        "snippet": content[:500] + "..." if len(content) > 500 else content
                    })
            except: pass

    print(json.dumps({"documentation_files": found_docs}, indent=2))

if __name__ == "__main__": main()
