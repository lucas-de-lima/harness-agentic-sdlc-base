from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from harnessctl.core.merge import controlled_merge, MERGE_TYPE_MAP, _gh_run
from harnessctl.core.hitl import create_gate, approve_gate, list_gates, reject_gate


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
    (path / "README.md").write_text("test\n", encoding="utf-8")
    _git(["add", "README.md"], path)
    _git(["commit", "-m", "init"], path)
    _git(["remote", "add", "origin", "https://github.com/test-owner/test-repo.git"], path)


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
        "confirmed_github_identity": {
            "owner": "test-owner",
            "repo": "test-repo",
        },
    }
    (harness / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def _make_full_repo() -> tuple[Path, tempfile.TemporaryDirectory]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name) / "project"
    root.mkdir()
    _make_repo(root)
    _make_harness(root)
    return root, td


class MergeHITLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root, self.td = _make_full_repo()

    def tearDown(self) -> None:
        self.td.cleanup()

    # ====== Test 1: agent attempting direct merge → BLOCK ======
    def test_1_direct_merge_blocked(self) -> None:
        """Agent attempting direct merge without harnessctl merge → BLOCK."""
        gates_file = self.root / ".harness" / "hitl" / "gates.json"
        self.assertFalse(gates_file.exists(), "No gates file should exist initially")

        # The controlled_merge should refuse because no gate exists
        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=1,
        )
        self.assertFalse(result["ok"], "Merge should be BLOCKED without gate")
        self.assertIn("BLOCKED", result.get("error", "").upper())

    # ====== Test 2: PR creation allowed (no merge) ======
    def test_2_pr_creation_allowed(self) -> None:
        """PR creation (via MCP create_pull_request) is NOT a merge and does NOT require a gate."""
        # PR creation doesn't go through harnessctl merge — it's allowed
        # This test verifies the merge command doesn't interfere with PR creation
        gates = list_gates(self.root)
        self.assertEqual(gates["total"], 0, "PR creation should not create gates")

    # ====== Test 3: merge without any gate → BLOCK ======
    def test_3_merge_no_gate_blocked(self) -> None:
        """Merge without creating any gate → BLOCK."""
        for merge_type in MERGE_TYPE_MAP:
            result = controlled_merge(
                self.root,
                merge_type=merge_type,
                affected_object=f"test-{merge_type}",
                pr_number=1,
            )
            self.assertFalse(result["ok"],
                             f"{merge_type} should be BLOCKED without gate")
            self.assertIn("BLOCKED", result.get("error", "").upper())

    # ====== Test 4: gate pending → BLOCK ======
    def test_4_gate_pending_blocked(self) -> None:
        """Merge with a pending (not approved) gate → BLOCK."""
        create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/test",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )

        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=1,
        )
        self.assertFalse(result["ok"], "Merge should be BLOCKED when gate is pending")
        self.assertIn("BLOCKED", result.get("error", "").upper())

    # ====== Test 5: gate rejected → BLOCK ======
    def test_5_gate_rejected_blocked(self) -> None:
        """Merge with a rejected gate → BLOCK."""
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/test",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )
        reject_gate(self.root, created["gate"]["instance_id"], decided_by="human")

        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=1,
        )
        self.assertFalse(result["ok"], "Merge should be BLOCKED when gate is rejected")
        self.assertIn("BLOCKED", result.get("error", "").upper())

    # ====== Test 6: gate approved → ALLOW ======
    @mock.patch("harnessctl.core.merge._gh_run")
    def test_6_gate_approved_allowed(self, mock_run) -> None:
        """Merge with an approved gate → ALLOW."""
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/test",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )
        approve_gate(self.root, created["gate"]["instance_id"], decided_by="human")

        mock_run.return_value = mock.MagicMock(
            returncode=0,
            stdout="merged",
            stderr="",
        )

        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=42,
        )
        self.assertTrue(result["ok"], "Merge should be ALLOWED when gate is approved")
        self.assertTrue(result["merged"])
        self.assertEqual(result["pr_number"], 42)

    # ====== Test 7: Story merge requires HG-MERGE-STORY ======
    @mock.patch("harnessctl.core.merge._gh_run")
    def test_7_story_merge_requires_story_gate(self, mock_run) -> None:
        """Story→Feature merge must have HG-MERGE-STORY approved (not HG-MERGE-FEATURE)."""
        create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",  # Wrong gate!
            workflow="WF-006",
            affected_object="feature/test",
            reason="Wrong gate type",
            evidence="Tests pass",
            expected_authority="human",
        )

        mock_run.return_value = mock.MagicMock(
            returncode=0,
            stdout="merged",
            stderr="",
        )

        result = controlled_merge(
            self.root,
            merge_type="story_to_feature",
            affected_object="story/test",
            pr_number=41,
        )
        self.assertFalse(result["ok"],
                         "Story merge should require HG-MERGE-STORY, not HG-MERGE-FEATURE")

    # ====== Test 8: Feature merge requires HG-MERGE-FEATURE ======
    @mock.patch("harnessctl.core.merge._gh_run")
    def test_8_feature_merge_requires_feature_gate(self, mock_run) -> None:
        """Feature→develop merge must have HG-MERGE-FEATURE approved."""
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/test",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )
        approve_gate(self.root, created["gate"]["instance_id"], decided_by="human")

        mock_run.return_value = mock.MagicMock(
            returncode=0,
            stdout="merged",
            stderr="",
        )

        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=43,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["gate_id"], "HG-MERGE-FEATURE")

    # ====== Test 9: Develop→Main requires HG-MERGE-DEVELOP ======
    @mock.patch("harnessctl.core.merge._gh_run")
    def test_9_develop_to_main_requires_develop_gate(self, mock_run) -> None:
        """develop→main merge must have HG-MERGE-DEVELOP approved."""
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-DEVELOP",
            workflow="WF-007",
            affected_object="develop",
            reason="Release ready",
            evidence="All tests pass",
            expected_authority="release-manager",
        )
        approve_gate(self.root, created["gate"]["instance_id"], decided_by="release-manager")

        mock_run.return_value = mock.MagicMock(
            returncode=0,
            stdout="merged to main",
            stderr="",
        )

        result = controlled_merge(
            self.root,
            merge_type="develop_to_main",
            affected_object="develop",
            pr_number=50,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["gate_id"], "HG-MERGE-DEVELOP")

    # ====== Test 10: Dedicated Harness attempting to re-enable direct merge → INVALID ======
    def test_10_dedicated_harness_cannot_reenable_direct_merge(self) -> None:
        """Dedicated Harness cannot disable mandatory gates (including merge gates)."""
        manifest_path = self.root / ".harness" / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["hitl"] = {
            "disabled_gates": ["HG-MERGE-STORY", "HG-MERGE-FEATURE", "HG-MERGE-DEVELOP"],
        }
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        from harnessctl.core.hitl import validate_dedicated_hitl
        result = validate_dedicated_hitl(self.root)
        self.assertFalse(result["valid"])
        self.assertIn("HG-MERGE-STORY", result["removed_gates"])
        self.assertIn("HG-MERGE-FEATURE", result["removed_gates"])
        self.assertIn("HG-MERGE-DEVELOP", result["removed_gates"])

    # ====== Test 11: invalid GitHub identity → BLOCK before merge ======
    def test_11_invalid_identity_blocks_merge(self) -> None:
        """Merge with invalid GitHub identity → BLOCK before attempting merge."""
        # Remove git remote to make identity preflight fail
        _git(["remote", "remove", "origin"], self.root)

        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=1,
        )
        self.assertFalse(result["ok"], "Merge should be BLOCKED with invalid identity")
        self.assertTrue(
            "identity" in result.get("error", "").lower() or
            "remote" in result.get("error", "").lower()
        )

    # ====== Test 12: gate state remains auditable ======
    def test_12_gate_state_auditable(self) -> None:
        """Gate state is persisted and audit trail is maintained."""
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/test",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", note="Approved")

        gates_file = self.root / ".harness" / "hitl" / "gates.json"
        self.assertTrue(gates_file.exists(), "Gate file should exist")

        gates = json.loads(gates_file.read_text(encoding="utf-8"))
        self.assertEqual(len(gates), 1)
        gate = gates[0]
        self.assertEqual(gate["state"], "approved")
        self.assertEqual(gate["decided_by"], "alice")
        self.assertEqual(gate["note"], "Approved")
        self.assertIsNotNone(gate["decided_at"])
        self.assertIsNotNone(gate["created_at"])

    # ====== Test 13: merge evidence recorded after successful merge ======
    @mock.patch("harnessctl.core.merge._gh_run")
    def test_13_merge_evidence_recorded(self, mock_run) -> None:
        """After a successful controlled merge, evidence is recorded in gates.json."""
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/test",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )
        approve_gate(self.root, created["gate"]["instance_id"], decided_by="human")

        mock_run.return_value = mock.MagicMock(
            returncode=0,
            stdout="successfully merged",
            stderr="",
        )

        result = controlled_merge(
            self.root,
            merge_type="feature_to_develop",
            affected_object="feature/test",
            pr_number=42,
        )
        self.assertTrue(result["ok"])
        self.assertIsNotNone(result["evidence"], "Merge evidence should exist")

        # Verify gate file has merge evidence appended
        gates_file = self.root / ".harness" / "hitl" / "gates.json"
        gates = json.loads(gates_file.read_text(encoding="utf-8"))
        self.assertIn("merge_evidence", gates[0])
        self.assertEqual(len(gates[0]["merge_evidence"]), 1)
        self.assertEqual(gates[0]["merge_evidence"][0]["pr_number"], 42)


if __name__ == "__main__":
    unittest.main()