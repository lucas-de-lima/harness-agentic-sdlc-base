import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_skill_layout():
    skill = ROOT / ".codex/skills/project-discovery"
    assert (skill / "SKILL.md").exists()


def test_skill_validation():
    result = subprocess.run(
        [sys.executable, "scripts/validate_skill.py", ".codex/skills/project-discovery"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
