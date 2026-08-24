from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

IGNORED_DIRS = {
    ".git", ".github", ".idea", ".vscode", "node_modules",
    "vendor", "dist", "build", "coverage", ".next", ".venv", "venv"
}

SPEC_HINTS = {
    ".md", ".markdown", ".txt"
}

def inventory(root: Path) -> dict:
    files = []
    dirs = set()
    extensions = {}
    for current, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        current_path = Path(current)
        if current_path != root:
            dirs.add(str(current_path.relative_to(root)))
        for name in filenames:
            p = current_path / name
            rel = p.relative_to(root)
            files.append(str(rel))
            ext = p.suffix.lower() or "<none>"
            extensions[ext] = extensions.get(ext, 0) + 1

    files.sort()
    return {
        "file_count": len(files),
        "directory_count": len(dirs),
        "extensions": dict(sorted(extensions.items())),
        "top_level": sorted({Path(f).parts[0] for f in files if Path(f).parts}),
        "sample_files": files[:200],
    }

def candidate_specs(root: Path) -> list[str]:
    candidates = []
    for path in root.iterdir():
        if path.is_file() and path.suffix.lower() in SPEC_HINTS:
            name = path.name.lower()
            score = 0
            for hint in ["readme", "spec", "project", "require", "requirements", "description"]:
                if hint in name:
                    score += 1
            candidates.append((score, path.name))
    candidates.sort(key=lambda x: (-x[0], x[1].lower()))
    return [name for _, name in candidates]

def detect_stack(inv: dict) -> list[str]:
    exts = inv["extensions"]
    stack = []
    if ".go" in exts or "go.mod" in inv["sample_files"]:
        stack.append("Go")
    if ".js" in exts or ".mjs" in exts or ".cjs" in exts or ".ts" in exts:
        stack.append("JavaScript/TypeScript")
    if ".py" in exts:
        stack.append("Python")
    if ".java" in exts:
        stack.append("Java")
    if ".rs" in exts:
        stack.append("Rust")
    return stack

def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only inventory of a real project.")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    project = args.project.resolve()
    output = args.output.resolve()

    if not project.is_dir():
        print("Project does not exist:", project)
        return 1
    if not (project / ".git").exists():
        print("Target is not a Git repository:", project)
        return 1

    inv = inventory(project)
    specs = candidate_specs(project)
    result = {
        "project_root": str(project),
        "inventory": inv,
        "candidate_specifications": specs,
        "detected_stack": detect_stack(inv),
        "git_present": True,
    }

    output.mkdir(parents=True, exist_ok=True)
    (output / "repository-inventory.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
