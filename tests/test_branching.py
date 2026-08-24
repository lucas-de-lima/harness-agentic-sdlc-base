from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from harnessctl.core.branching import check_branch, _classify_branch, _validate_branch_name


def _git(args: list[str], cwd: Path) -> str:
    env = dict(os.environ)
    env["GIT_AUTHOR_NAME"] = "test"
    env["GIT_AUTHOR_EMAIL"] = "test@test.test"
    env["GIT_COMMITTER_NAME"] = "test"
    env["GIT_COMMITTER_EMAIL"] = "test@test.test"
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    ).stdout.strip()


def _make_repo(path: Path) -> None:
    _git(["init", "--initial-branch=main"], path)
    _git(["config", "user.name", "test"], path)
    _git(["config", "user.email", "test@test.test"], path)


def _commit(path: Path, msg: str = "init") -> None:
    (path / "README.md").write_text("test\n", encoding="utf-8")
    _git(["add", "README.md"], path)
    _git(["commit", "-m", msg], path)


class BranchClassificationTests(unittest.TestCase):
    def test_classify_main(self) -> None:
        self.assertEqual(_classify_branch("main"), "main")

    def test_classify_master(self) -> None:
        self.assertEqual(_classify_branch("master"), "main")

    def test_classify_develop(self) -> None:
        self.assertEqual(_classify_branch("develop"), "develop")

    def test_classify_feature(self) -> None:
        self.assertEqual(_classify_branch("feature/auth"), "feature")

    def test_classify_story(self) -> None:
        self.assertEqual(_classify_branch("story/register"), "story")

    def test_classify_hotfix(self) -> None:
        self.assertEqual(_classify_branch("hotfix/urgent"), "hotfix")

    def test_classify_unknown(self) -> None:
        self.assertEqual(_classify_branch("random-branch"), "unknown")

    def test_validate_valid_names(self) -> None:
        for name in [
            "main",
            "develop",
            "feature/authentication-session",
            "story/register-new-user",
            "hotfix/critical-fix",
        ]:
            self.assertTrue(_validate_branch_name(name), f"Expected valid: {name}")

    def test_validate_invalid_names(self) -> None:
        for name in ["random", "wip/stuff", "experiment/test", "FEATURE/Upper"]:
            self.assertFalse(_validate_branch_name(name), f"Expected invalid: {name}")


class BranchCheckIntegrationTests(unittest.TestCase):
    def test_not_a_git_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "not-a-repo"
            root.mkdir()
            result = check_branch(root)
            self.assertFalse(result.ok)
            self.assertTrue(any("Git repository" in e for e in result.errors))

    def test_main_branch_ok(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            result = check_branch(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.branch_type, "main")
            self.assertTrue(result.main_exists)

    def test_develop_branch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["branch", "develop"], root)
            _git(["checkout", "develop"], root)
            result = check_branch(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.branch_type, "develop")

    def test_feature_branch_from_develop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["branch", "develop"], root)
            _git(["checkout", "develop"], root)
            _git(["checkout", "-b", "feature/authentication"], root)
            _commit(root, "feature work")
            result = check_branch(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.branch_type, "feature")
            self.assertEqual(result.expected_parent, "develop")

    def test_feature_branch_without_develop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["checkout", "-b", "feature/auth"], root)
            result = check_branch(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("develop" in e for e in result.errors),
                f"Expected develop error: {result.errors}",
            )

    def test_story_branch_from_feature(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["branch", "develop"], root)
            _git(["checkout", "develop"], root)
            _git(["checkout", "-b", "feature/auth"], root)
            _git(["checkout", "-b", "story/register"], root)
            _git(["branch", "--set-upstream-to=feature/auth", "story/register"], root)
            result = check_branch(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.branch_type, "story")
            self.assertEqual(result.actual_parent, "feature/auth")

    def test_story_branch_wrong_parent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["branch", "develop"], root)
            _git(["checkout", "develop"], root)
            _git(["checkout", "-b", "story/register", "develop"], root)
            _git(["branch", "--set-upstream-to=develop", "story/register"], root)
            result = check_branch(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("feature" in e for e in result.errors),
                f"Expected feature-parent error: {result.errors}",
            )

    def test_unknown_branch_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["checkout", "-b", "wip/random"], root)
            result = check_branch(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("branching model" in e for e in result.errors),
                f"Expected model error: {result.errors}",
            )

    def test_hotfix_branch_from_main(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            _git(["checkout", "-b", "hotfix/critical", "main"], root)
            _commit(root, "hotfix work")
            result = check_branch(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.branch_type, "hotfix")
            self.assertEqual(result.expected_parent, "main")

    def test_expected_branch_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _commit(root)
            result = check_branch(root, expected_branch="develop")
            self.assertFalse(result.ok)
            self.assertTrue(
                any("Expected branch" in e for e in result.errors),
                f"Expected branch mismatch error: {result.errors}",
            )

    def test_no_main_branch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _git(["init", "--initial-branch=custom"], root)
            _git(["config", "user.name", "test"], root)
            _git(["config", "user.email", "test@test.test"], root)
            _commit(root)
            result = check_branch(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("'main'" in e for e in result.errors),
                f"Expected missing main error: {result.errors}",
            )


if __name__ == "__main__":
    unittest.main()
