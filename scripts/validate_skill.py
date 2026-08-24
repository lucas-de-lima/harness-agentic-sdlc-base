from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required.")
    raise SystemExit(2)

ALLOWED = {"name", "description", "license", "allowed-tools", "metadata"}


def validate(skill_dir: Path) -> tuple[bool, str]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML: {exc}"

    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a mapping"

    unexpected = set(frontmatter) - ALLOWED
    if unexpected:
        return False, f"Unexpected frontmatter keys: {sorted(unexpected)}"

    for key in ("name", "description"):
        if not isinstance(frontmatter.get(key), str) or not frontmatter[key].strip():
            return False, f"Missing or empty {key}"

    name = frontmatter["name"]
    if name != skill_dir.name:
        return False, f"name '{name}' does not match directory '{skill_dir.name}'"

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        return False, "Invalid skill name"

    return True, "valid"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_skill.py <skill-directory>")
        raise SystemExit(2)
    ok, message = validate(Path(sys.argv[1]))
    print(message)
    raise SystemExit(0 if ok else 1)
