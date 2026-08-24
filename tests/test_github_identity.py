from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from harnessctl.core.github_identity import preflight_github
from harnessctl.core.gitignore import generate_gitignore, validate_gitignore


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


def _make_harness(root: Path) -> None:
    harness = root / ".harness"
    harness.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": "1",
        "harness_version": "0.1.0",
        "base_harness_version": "0.29.0",
        "project_repository": "test-repo",
        "architecture_profile": "test",
        "selected_agents": [],
        "selected_skills": [],
        "selected_tools": [],
        "enabled_workflows": [],
        "confirmed_github_identity": None,
    }
    (harness / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


class GitHubIdentityPreflightTests(unittest.TestCase):
    def test_correct_origin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "misleading-folder-name"
            root.mkdir()
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "git@github.com:correct-owner/correct-repo.git"],
                root,
            )
            result = preflight_github(root)
            self.assertTrue(result.ok, f"Expected ok but got errors: {result.errors}")
            self.assertEqual(result.canonical_owner, "correct-owner")
            self.assertEqual(result.canonical_repo, "correct-repo")
            self.assertEqual(result.origin.owner, "correct-owner")

    def test_no_origin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            result = preflight_github(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("origin" in e for e in result.errors),
                f"Expected 'origin' in errors: {result.errors}",
            )

    def test_divergent_owner_from_harness(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "git@github.com:actual-owner/actual-repo.git"],
                root,
            )
            _make_harness(root)
            manifest_path = root / ".harness" / "manifest.json"
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            data["confirmed_github_identity"] = {
                "owner": "wrong-owner",
                "repo": "actual-repo",
            }
            manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            result = preflight_github(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("divergence" in e or "diverge" in e.lower() for e in result.errors),
                f"Expected divergence in errors: {result.errors}",
            )

    def test_divergent_from_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "git@github.com:real-owner/real-repo.git"],
                root,
            )
            result = preflight_github(
                root, expected_owner="wrong-owner", expected_repo="real-repo"
            )
            self.assertFalse(result.ok)
            self.assertTrue(
                any("divergence" in e or "diverge" in e.lower() for e in result.errors),
                f"Expected divergence in errors: {result.errors}",
            )

    def test_misleading_path_not_used(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "re-aproveitamento" / "projects" / "blogs-api"
            root.mkdir(parents=True)
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "git@github.com:target-org/target-repo.git"],
                root,
            )
            result = preflight_github(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.canonical_owner, "target-org")
            self.assertEqual(result.canonical_repo, "target-repo")
            self.assertNotEqual(result.canonical_owner, "re-aproveitamento")
            self.assertNotEqual(result.canonical_repo, "blogs-api")

    def test_https_origin_url(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "https://github.com/some-owner/some-repo.git"],
                root,
            )
            result = preflight_github(root)
            self.assertTrue(result.ok, f"Expected ok: {result.errors}")
            self.assertEqual(result.canonical_owner, "some-owner")
            self.assertEqual(result.canonical_repo, "some-repo")

    def test_record_identity(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "git@github.com:my-org/my-repo.git"],
                root,
            )
            _make_harness(root)
            result = preflight_github(root, record=True)
            self.assertTrue(result.ok)
            manifest = json.loads(
                (root / ".harness" / "manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                manifest["confirmed_github_identity"],
                {"owner": "my-org", "repo": "my-repo"},
            )

    def test_non_github_origin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "project"
            root.mkdir()
            _make_repo(root)
            _git(
                ["remote", "add", "origin", "git@gitlab.com:some/repo.git"],
                root,
            )
            result = preflight_github(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("origin" in e for e in result.errors),
                f"Expected origin error: {result.errors}",
            )

    def test_not_a_git_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "not-a-repo"
            root.mkdir()
            result = preflight_github(root)
            self.assertFalse(result.ok)
            self.assertTrue(
                any("Git repository" in e for e in result.errors),
                f"Expected 'not a Git repository' error: {result.errors}",
            )


class GitignoreTests(unittest.TestCase):
    def test_generate_go_gitignore(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            result = generate_gitignore(root, "go")
            self.assertTrue(result["valid"])
            self.assertEqual(result["action"], "created")
            self.assertEqual(result["language"], "go")
            content = (root / ".gitignore").read_text(encoding="utf-8")
            self.assertIn("*.exe", content)
            self.assertIn("vendor/", content)
            self.assertIn(".env", content)

    def test_validate_go_gitignore(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            generate_gitignore(root, "go")
            result = validate_gitignore(root / ".gitignore", "go")
            self.assertTrue(result["valid"])
            self.assertEqual(result["language"], "go")

    def test_validate_go_gitignore_missing_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".gitignore").write_text("only this\n", encoding="utf-8")
            result = validate_gitignore(root / ".gitignore", "go")
            self.assertFalse(result["valid"])
            self.assertIn("*.exe", result["missing_patterns"])

    def test_generate_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".gitignore").write_text("existing\n", encoding="utf-8")
            result = generate_gitignore(root, "go")
            self.assertFalse(result["valid"])
            self.assertEqual(result["action"], "exists")

    def test_generate_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            generate_gitignore(root, "go")
            result = generate_gitignore(root, "go")
            self.assertTrue(result["valid"])
            self.assertEqual(result["action"], "unchanged")

    def test_language_alias(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            result = generate_gitignore(root, "golang")
            self.assertEqual(result["language"], "go")

    def test_unknown_language_falls_back(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            result = generate_gitignore(root, "rust")
            self.assertTrue(result["valid"])
            self.assertEqual(result["language"], "generic")


if __name__ == "__main__":
    unittest.main()
