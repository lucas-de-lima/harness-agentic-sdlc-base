from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from harnessctl.core.hitl import (
    create_gate,
    approve_gate,
    reject_gate,
    resume_check,
    list_gates,
    check_merge_allowed,
    validate_dedicated_hitl,
    MANDATORY_GATES,
)


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


def _make_full_repo() -> tuple[Path, tempfile.TemporaryDirectory]:
    td = tempfile.TemporaryDirectory()
    root = Path(td.name) / "project"
    root.mkdir()
    _make_repo(root)
    _make_harness(root)
    return root, td


class HITLTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root, self.td = _make_full_repo()

    def tearDown(self) -> None:
        self.td.cleanup()

    def test_1_pr_creation_allowed_no_gate_needed(self) -> None:
        result = check_merge_allowed(self.root, "story_to_feature", "story/test")
        self.assertFalse(result["allowed"])
        self.assertIn("BLOCKED", result["error"])

    def test_2_merge_automatic_blocked(self) -> None:
        result = check_merge_allowed(self.root, "feature_to_develop", "feature/auth")
        self.assertFalse(result["allowed"])
        self.assertIn("BLOCKED", result["error"])

    def test_3_story_complete_pauses_at_human_gate(self) -> None:
        result = create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/register-user",
            reason="Story implementation complete; merge to feature/auth requires human approval.",
            evidence="Tests pass, review approved.",
            expected_authority="human-reviewer",
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["gate"]["state"], "pending")
        self.assertEqual(result["gate"]["gate_id"], "HG-MERGE-STORY")
        gates = list_gates(self.root, state_filter="pending")
        self.assertEqual(gates["total"], 1)

    def test_4_human_approval_allows_resume(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/register-user",
            reason="Story complete",
            evidence="Tests pass",
            expected_authority="human-reviewer",
        )
        instance_id = created["gate"]["instance_id"]

        resume_before = resume_check(self.root, instance_id)
        self.assertFalse(resume_before["can_resume"])
        self.assertEqual(resume_before["gate"]["state"], "pending")

        approved = approve_gate(self.root, instance_id, decided_by="alice")
        self.assertTrue(approved["ok"])
        self.assertEqual(approved["gate"]["state"], "approved")
        self.assertEqual(approved["gate"]["decided_by"], "alice")

        resume_after = resume_check(self.root, instance_id)
        self.assertTrue(resume_after["can_resume"])
        self.assertEqual(resume_after["gate"]["state"], "approved")

    def test_5_human_rejection_returns_to_correct_state(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/register-user",
            reason="Story complete",
            evidence="Tests pass",
            expected_authority="human-reviewer",
        )
        instance_id = created["gate"]["instance_id"]

        rejected = reject_gate(self.root, instance_id, decided_by="bob", note="Found issues")
        self.assertTrue(rejected["ok"])
        self.assertEqual(rejected["gate"]["state"], "rejected")
        self.assertEqual(rejected["gate"]["decided_by"], "bob")
        self.assertEqual(rejected["gate"]["note"], "Found issues")
        self.assertEqual(rejected["resume_target"], "story_in_progress")

        resume = resume_check(self.root, instance_id)
        self.assertFalse(resume["can_resume"])
        self.assertEqual(resume["resume_target"], "story_in_progress")

    def test_6_feature_complete_pauses_before_develop_merge(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/auth",
            reason="Feature complete; all Stories Done; merge to develop requires human approval.",
            evidence="Integration tests pass, all stories reviewed.",
            expected_authority="human-reviewer",
        )
        self.assertTrue(created["ok"])
        self.assertEqual(created["gate"]["gate_id"], "HG-MERGE-FEATURE")

        merge_check = check_merge_allowed(self.root, "feature_to_develop", "feature/auth")
        self.assertFalse(merge_check["allowed"])
        self.assertEqual(merge_check["gate"]["state"], "pending")

    def test_7_release_candidate_pauses_before_main(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-RELEASE",
            workflow="WF-007",
            affected_object="develop",
            reason="Release candidate ready; release requires human approval.",
            evidence="All features merged, release tests pass.",
            expected_authority="release-manager",
        )
        self.assertTrue(created["ok"])

        develop_merge = create_gate(
            self.root,
            gate_id="HG-MERGE-DEVELOP",
            workflow="WF-007",
            affected_object="develop",
            reason="Merge develop to main for release.",
            evidence="Release approved.",
            expected_authority="release-manager",
        )
        self.assertTrue(develop_merge["ok"])

        gates = list_gates(self.root, state_filter="pending")
        self.assertEqual(gates["total"], 2)

    def test_8_architecture_decision_requires_hitl(self) -> None:
        result = create_gate(
            self.root,
            gate_id="HG-ARCHITECTURE",
            workflow="WF-005",
            affected_object="ADR-002",
            reason="Implementation revealed architecture is insufficient; ADR update required.",
            evidence="Current A2 does not support the required integration.",
            expected_authority="architect",
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["gate"]["gate_id"], "HG-ARCHITECTURE")
        self.assertEqual(result["gate"]["state"], "pending")

    def test_9_paused_workflow_resumes_without_duplicate_work(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/auth",
            reason="Feature complete",
            evidence="All stories done",
            expected_authority="human",
        )
        instance_id = created["gate"]["instance_id"]

        resume_pending = resume_check(self.root, instance_id)
        self.assertFalse(resume_pending["can_resume"])
        self.assertEqual(resume_pending["gate"]["state"], "pending")

        approve_gate(self.root, instance_id, decided_by="alice")

        resume_approved = resume_check(self.root, instance_id)
        self.assertTrue(resume_approved["can_resume"])

        all_gates = list_gates(self.root)
        self.assertEqual(all_gates["total"], 1)
        self.assertEqual(all_gates["gates"][0]["state"], "approved")

    def test_10_dedicated_harness_cannot_remove_mandatory_gate(self) -> None:
        manifest_path = self.root / ".harness" / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["hitl"] = {
            "disabled_gates": ["HG-MERGE-STORY", "HG-RELEASE"],
        }
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        result = validate_dedicated_hitl(self.root)
        self.assertFalse(result["valid"])
        self.assertIn("HG-MERGE-STORY", result["removed_gates"])
        self.assertIn("HG-RELEASE", result["removed_gates"])

    def test_10b_dedicated_harness_clean_hitl_config(self) -> None:
        manifest_path = self.root / ".harness" / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["hitl"] = {
            "disabled_gates": [],
            "approvers": {"HG-RELEASE": "release-manager"},
        }
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        result = validate_dedicated_hitl(self.root)
        self.assertTrue(result["valid"])
        self.assertEqual(result["removed_gates"], [])

    def test_10c_dedicated_harness_no_hitl_config(self) -> None:
        result = validate_dedicated_hitl(self.root)
        self.assertTrue(result["valid"])
        self.assertEqual(result["removed_gates"], [])

    def test_duplicate_gate_for_same_object_blocked(self) -> None:
        create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/test",
            reason="r1",
            evidence="e1",
            expected_authority="human",
        )
        result = create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/test",
            reason="r2",
            evidence="e2",
            expected_authority="human",
        )
        self.assertFalse(result["ok"])
        self.assertIn("already exists", result["error"])

    def test_unknown_gate_id_rejected(self) -> None:
        result = create_gate(
            self.root,
            gate_id="HG-UNKNOWN",
            workflow="WF-005",
            affected_object="x",
            reason="r",
            evidence="e",
            expected_authority="human",
        )
        self.assertFalse(result["ok"])
        self.assertIn("Unknown gate_id", result["error"])

    def test_cannot_approve_already_decided_gate(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/test",
            reason="r",
            evidence="e",
            expected_authority="human",
        )
        instance_id = created["gate"]["instance_id"]
        approve_gate(self.root, instance_id, decided_by="alice")

        result = approve_gate(self.root, instance_id, decided_by="bob")
        self.assertFalse(result["ok"])
        self.assertIn("already approved", result["error"])

    def test_resume_nonexistent_gate(self) -> None:
        result = resume_check(self.root, "hitl_nonexistent")
        self.assertFalse(result["ok"])
        self.assertIn("not found", result["error"])

    def test_all_mandatory_gates_present(self) -> None:
        expected = {
            "HG-PRODUCT",
            "HG-ARCHITECTURE",
            "HG-SCOPE",
            "HG-MERGE-STORY",
            "HG-MERGE-FEATURE",
            "HG-MERGE-DEVELOP",
            "HG-RELEASE",
            "HG-SECURITY-EXCEPTION",
            "HG-DESTRUCTIVE",
            "HG-DEPLOY",
        }
        self.assertEqual(MANDATORY_GATES, expected)

    def test_gate_audit_trail_persisted(self) -> None:
        created = create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/test",
            reason="r",
            evidence="e",
            expected_authority="human",
        )
        instance_id = created["gate"]["instance_id"]

        gates_file = self.root / ".harness" / "hitl" / "gates.json"
        self.assertTrue(gates_file.exists())

        approve_gate(self.root, instance_id, decided_by="alice", note="Looks good")

        data = json.loads(gates_file.read_text(encoding="utf-8"))
        self.assertEqual(len(data), 1)
        gate = data[0]
        self.assertEqual(gate["state"], "approved")
        self.assertEqual(gate["decided_by"], "alice")
        self.assertEqual(gate["note"], "Looks good")
        self.assertIsNotNone(gate["decided_at"])
        self.assertIsNotNone(gate["created_at"])


if __name__ == "__main__":
    unittest.main()
