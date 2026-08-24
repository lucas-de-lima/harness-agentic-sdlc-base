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
    reconcile_gate,
    record_manual_merge,
    MANDATORY_GATES,
    PR_STATES,
    MERGE_ORIGINS,
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


class HITLResumabilityTests(unittest.TestCase):

    def setUp(self) -> None:
        self.root, self.td = _make_full_repo()

    def tearDown(self) -> None:
        self.td.cleanup()

    def _create_story_gate(self) -> dict:
        return create_gate(
            self.root,
            gate_id="HG-MERGE-STORY",
            workflow="WF-006",
            affected_object="story/register-user",
            reason="Story implementation complete; merge requires human approval.",
            evidence="Tests pass, review approved.",
            expected_authority="human-reviewer",
        )

    def _create_feature_gate(self) -> dict:
        return create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/auth",
            reason="Feature complete; merge to develop requires human approval.",
            evidence="All stories done, integration tests pass.",
            expected_authority="human-reviewer",
        )

    # Test 1: gate pending + PR open -> workflow pauses
    def test_1_gate_pending_pr_open_workflow_pauses(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = resume_check(self.root, instance_id, pr_state="OPEN")

        self.assertFalse(result["can_resume"])
        self.assertEqual(result["gate"]["state"], "pending")
        self.assertEqual(result["pr_state"], "OPEN")
        self.assertIn("PAUSED", result["message"])

    # Test 2: humano faz merge manual -> resume detecta MERGED e continua
    def test_2_human_manual_merge_detected_on_resume(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = resume_check(self.root, instance_id, pr_state="MERGED")

        self.assertTrue(result["can_resume"])
        self.assertEqual(result["pr_state"], "MERGED")
        self.assertEqual(result["merge_origin"], "human_manual")
        self.assertIn("already merged", result["message"])

    # Test 3: gate approved + PR open -> Harness-controlled merge permitido
    def test_3_gate_approved_pr_open_merge_allowed(self) -> None:
        created = self._create_feature_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="harness_controlled")

        resume = resume_check(self.root, instance_id, pr_state="OPEN")
        self.assertTrue(resume["can_resume"])
        self.assertEqual(resume["merge_origin"], "harness_controlled")

        merge_check = check_merge_allowed(self.root, "feature_to_develop", "feature/auth", pr_state="OPEN")
        self.assertTrue(merge_check["allowed"])
        self.assertEqual(merge_check["merge_origin"], "harness_controlled")

    # Test 4: gate approved + PR already merged -> nenhum segundo merge
    def test_4_gate_approved_pr_already_merged_no_second_merge(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice")

        result = resume_check(self.root, instance_id, pr_state="MERGED")
        self.assertTrue(result["can_resume"])
        self.assertEqual(result["pr_state"], "MERGED")
        self.assertIn("already merged", result["message"])

        merge_check = check_merge_allowed(self.root, "story_to_feature", "story/register-user", pr_state="MERGED")
        self.assertTrue(merge_check["allowed"])
        self.assertEqual(merge_check["pr_state"], "MERGED")
        self.assertIn("already merged", merge_check["message"])

    # Test 5: PR closed sem merge -> fluxo de correcao
    def test_5_pr_closed_without_merge_returns_to_correction(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = resume_check(self.root, instance_id, pr_state="CLOSED")
        self.assertFalse(result["can_resume"])
        self.assertEqual(result["pr_state"], "CLOSED")
        self.assertEqual(result["resume_target"], "story_in_progress")
        self.assertIn("correction", result["message"])

        merge_check = check_merge_allowed(self.root, "story_to_feature", "story/register-user", pr_state="CLOSED")
        self.assertFalse(merge_check["allowed"])
        self.assertIn("BLOCKED", merge_check["error"])

    # Test 6: Story -> Done antes do merge
    def test_6_story_done_before_merge_reflected_on_resume(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice")

        resume = resume_check(self.root, instance_id, pr_state="OPEN")
        self.assertTrue(resume["can_resume"])
        self.assertEqual(resume["gate"]["state"], "approved")

    # Test 7: Story -> Closed apos merge (simulado via PR MERGED)
    def test_7_story_closed_after_merge(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        record_manual_merge(self.root, instance_id, decided_by="alice", pr_number=42)

        gates = list_gates(self.root)
        gate = gates["gates"][0]
        self.assertEqual(gate["state"], "approved")
        self.assertEqual(gate["merge_origin"], "human_manual")
        self.assertEqual(len(gate["merge_evidence"]), 1)
        self.assertEqual(gate["merge_evidence"][0]["pr_number"], 42)

    # Test 8: Feature -> Done antes do merge em develop
    def test_8_feature_done_before_develop_merge(self) -> None:
        created = self._create_feature_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="harness_controlled")

        resume = resume_check(self.root, instance_id, pr_state="OPEN")
        self.assertTrue(resume["can_resume"])
        self.assertEqual(resume["gate"]["state"], "approved")
        self.assertEqual(resume["merge_origin"], "harness_controlled")

    # Test 9: Feature -> Closed apos merge em develop
    def test_9_feature_closed_after_develop_merge(self) -> None:
        created = self._create_feature_gate()
        instance_id = created["gate"]["instance_id"]

        record_manual_merge(self.root, instance_id, decided_by="alice", pr_number=45)

        gates = list_gates(self.root)
        gate = gates["gates"][0]
        self.assertEqual(gate["merge_origin"], "human_manual")
        self.assertEqual(gate["merge_evidence"][0]["pr_number"], 45)

    # Test 10: Project atualizado em cada transicao
    def test_10_gate_lifecycle_has_all_expected_fields(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="harness_controlled")

        gates = list_gates(self.root)
        gate = gates["gates"][0]
        self.assertEqual(gate["gate_id"], "HG-MERGE-STORY")
        self.assertEqual(gate["state"], "approved")
        self.assertEqual(gate["merge_origin"], "harness_controlled")
        self.assertIsNotNone(gate["decided_at"])
        self.assertIsNotNone(gate["decided_by"])
        self.assertEqual(gate["decided_by"], "alice")

    # Test 11: divergencia GitHub/local -> BLOCK
    def test_11_divergence_detected_by_reconcile(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = reconcile_gate(self.root, instance_id, pr_state="MERGED")

        self.assertTrue(result["gate_found"])
        self.assertGreater(len(result["issues"]), 0)
        self.assertFalse(result["reconciled"])
        has_merge_origin_issue = any("merge_origin" in i for i in result["issues"])
        self.assertTrue(has_merge_origin_issue)

    # Test 12: ausencia de transicao duplicada
    def test_12_duplicate_gate_prevented(self) -> None:
        self._create_story_gate()
        result = self._create_story_gate()
        self.assertFalse(result["ok"])
        self.assertIn("already exists", result["error"])

    # Test 13: origem do merge registrada corretamente
    def test_13_merge_origin_recorded_correctly(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="human_manual")

        gates = list_gates(self.root)
        self.assertEqual(gates["gates"][0]["merge_origin"], "human_manual")

        created2 = create_gate(
            self.root,
            gate_id="HG-MERGE-FEATURE",
            workflow="WF-006",
            affected_object="feature/auth",
            reason="Feature complete",
            evidence="Tests pass",
            expected_authority="human",
        )
        instance_id2 = created2["gate"]["instance_id"]

        approve_gate(self.root, instance_id2, decided_by="bob", merge_origin="harness_controlled")

        gates2 = list_gates(self.root)
        feature_gate = [g for g in gates2["gates"] if g["gate_id"] == "HG-MERGE-FEATURE"][0]
        self.assertEqual(feature_gate["merge_origin"], "harness_controlled")

    # Test 14: Tasks permanecem sincronizadas (gate lifecycle for tasks)
    def test_14_task_consistency_validated(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = resume_check(self.root, instance_id)
        self.assertFalse(result["can_resume"])
        self.assertEqual(result["gate"]["affected_object"], "story/register-user")

        approve_gate(self.root, instance_id, decided_by="alice")

        gates_path = self.root / ".harness" / "hitl" / "gates.json"
        data = json.loads(gates_path.read_text(encoding="utf-8"))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["affected_object"], "story/register-user")

    # Test 15: Dedicated Harness herda comportamento
    def test_15_dedicated_harness_inherits_behavior(self) -> None:
        manifest_path = self.root / ".harness" / "manifest.json"
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["hitl"] = {"disabled_gates": [], "applicable_gates": list(MANDATORY_GATES)}
        manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="human_manual")

        resume = resume_check(self.root, instance_id, pr_state="MERGED")
        self.assertTrue(resume["can_resume"])
        self.assertEqual(resume["merge_origin"], "human_manual")

    # Test 16: Agent nunca executa merge direto fora do caminho controlado
    def test_16_agent_direct_merge_blocked(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = check_merge_allowed(self.root, "story_to_feature", "story/register-user")
        self.assertFalse(result["allowed"])
        self.assertIn("BLOCKED", result["error"])

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="harness_controlled")

        merge_check = check_merge_allowed(self.root, "story_to_feature", "story/register-user", pr_state="OPEN")
        self.assertTrue(merge_check["allowed"])
        self.assertEqual(merge_check["merge_origin"], "harness_controlled")

        merge_check_merged = check_merge_allowed(
            self.root, "story_to_feature", "story/register-user", pr_state="MERGED"
        )
        self.assertTrue(merge_check_merged["allowed"])

    # Additional: pr_state validation
    def test_invalid_pr_state_rejected(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = resume_check(self.root, instance_id, pr_state="INVALID")
        self.assertFalse(result["ok"])
        self.assertIn("Invalid pr_state", result["error"])

    # Additional: reconcile detects approved + open
    def test_reconcile_approved_gate_open_pr(self) -> None:
        created = self._create_feature_gate()
        instance_id = created["gate"]["instance_id"]

        approve_gate(self.root, instance_id, decided_by="alice", merge_origin="harness_controlled")

        result = reconcile_gate(self.root, instance_id, pr_state="OPEN")
        self.assertTrue(result["gate_found"])
        self.assertEqual(result["pr_state"], "OPEN")

    # Additional: reconcile detects closed without merge
    def test_reconcile_closed_without_merge(self) -> None:
        created = self._create_story_gate()
        instance_id = created["gate"]["instance_id"]

        result = reconcile_gate(self.root, instance_id, pr_state="CLOSED")
        self.assertTrue(result["gate_found"])

    # Additional: record_manual_merge with nonexistent gate
    def test_record_manual_merge_nonexistent_gate(self) -> None:
        result = record_manual_merge(self.root, "hitl_nonexistent", decided_by="alice")
        self.assertFalse(result["ok"])
        self.assertIn("not found", result["error"])


if __name__ == "__main__":
    unittest.main()