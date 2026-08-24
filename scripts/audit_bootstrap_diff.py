from pathlib import Path
import subprocess
import sys

ALLOWED_PREFIXES = [".harness/"]

def main():
    if len(sys.argv) != 2:
        print("usage: audit_bootstrap_diff.py <project-root>")
        return 2
    root = Path(sys.argv[1]).resolve()
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        print(result.stderr)
        return result.returncode

    unexpected = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip()
        if not any(path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
            unexpected.append(path)

    if unexpected:
        print("UNEXPECTED CHANGES")
        for p in unexpected:
            print("-", p)
        return 1

    print("EXPECTED: .harness/** only")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
