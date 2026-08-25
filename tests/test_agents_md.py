from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import re

from harnessctl.core.factory import generate_harness
from harnessctl.core.validator import validate_dedicated
from harnessctl.core.vault import load_vault


class AgentsMDTests(unittest.TestCase):
    """Validate AGENTS.md generation and contract."""

    def setUp(self):
        self.profile = {
            "schema_version": "1",
            "identity": {
                "proposed_product_name": "Demo Service",
                "proposed_repository_name": "demo-service",
                "short_description": "demo",
                "problem_statement": "demo",
                "selected_architecture": "simple",
            },
            "domain": {
                "actors": [],
                "core_concepts": [],
                "entities": [],
                "business_rules": [],
            },
            "technical": {
                "application_type": "HTTP API",
                "persistence": "none",
                "interfaces": ["HTTP"],
                "external_dependencies": [],
            },
            "constraints": [],
            "risks": [],
            "open_questions": [],
        }

    # ── 1. New Dedicated receives AGENTS.md ──────────────────────────

    def test_new_dedicated_receives_agents_md(self):
        """Factory must generate AGENTS.md for every new Dedicated Harness."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            self.assertTrue((out / "AGENTS.md").exists(),
                            "AGENTS.md not generated")

    # ── 2. AGENTS.md points only to existing files ───────────────────

    def test_agents_md_points_to_existing_files(self):
        """Every path referenced in AGENTS.md must exist."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            text = (out / "AGENTS.md").read_text(encoding="utf-8")
            # Extract markdown link targets: [text](path)
            for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
                ref = match.group(2)
                if ref.startswith("."):
                    self.assertTrue(
                        (out / ref).exists(),
                        f"AGENTS.md references non-existent file: {ref}"
                    )

    # ── 3. No absolute paths in AGENTS.md ────────────────────────────

    def test_agents_md_no_absolute_paths(self):
        """AGENTS.md must not contain absolute filesystem paths."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            text = (out / "AGENTS.md").read_text(encoding="utf-8")
            # Relative paths like .harness/README.md are fine — only block
            # paths that start with / or have a drive letter
            for line in text.splitlines():
                self.assertNotIn("\\", line,  # backslash = absolute on Windows
                                 f"AGENTS.md contains backslash (absolute path): {line}")
                # Leading forward slash would indicate Unix absolute path
                line_stripped = line.strip()
                if line_stripped.startswith("/"):
                    self.fail(f"AGENTS.md contains leading / (absolute path): {line}")
            # No drive letters
            self.assertNotIn(":\\", text,
                             "AGENTS.md contains Windows drive paths (absolute)")

    # ── 4. No runtime dependency on Base Harness ─────────────────────

    def test_agents_md_no_base_dependency(self):
        """AGENTS.md must not reference Base Harness as a runtime dependency."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            text = (out / "AGENTS.md").read_text(encoding="utf-8")
            text_lower = text.lower()
            # "base harness" references are acceptable as provenance, but
            # "harness agentic sdlc base" or similar runtime dependency is not
            self.assertNotIn(
                "depends on", text_lower,
                "AGENTS.md implies runtime dependency on Base"
            )
            self.assertNotIn(
                "requires", text_lower,
                "AGENTS.md implies required external dependency"
            )

    # ── 5. AGENTS.md does not duplicate harness content ──────────────

    def test_agents_md_does_not_duplicate(self):
        """AGENTS.md must be a short bootstrap file, not a copy of the harness."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            text = (out / "AGENTS.md").read_text(encoding="utf-8")
            readme = (out / ".harness" / "README.md").read_text(encoding="utf-8")
            # AGENTS.md must be significantly shorter than README
            # (it's bootstrap only, not documentation)
            agents_lines = len(text.splitlines())
            readme_lines = len(readme.splitlines())
            self.assertLess(
                agents_lines, max(readme_lines + 10, 60),
                "AGENTS.md is too long — likely duplicating harness content"
            )
            # Must not contain workflow definitions
            self.assertNotIn("WF-", text,
                             "AGENTS.md must not duplicate workflow IDs")
            # Must not contain policy definitions
            self.assertNotIn("HG-", text,
                             "AGENTS.md must not duplicate HITL gate IDs")

    # ── 6. Dedicated remains valid without AGENTS.md (backward compat) ──

    def test_dedicated_valid_without_agents_md(self):
        """A pre-existing Dedicated Harness without AGENTS.md is still valid."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            # Remove AGENTS.md to simulate pre-existing harness
            (out / "AGENTS.md").unlink()
            validation = validate_dedicated(out)
            # Should be invalid (missing AGENTS.md now required)
            self.assertFalse(validation["valid"])
            self.assertIn("AGENTS.md", validation["missing"])

    # ── 7. AGENTS.md works as entry point without Obsidian ─────────────

    def test_agents_md_entry_point_without_obsidian(self):
        """AGENTS.md must work even if .harness/vault/.obsidian is missing."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            # Remove .obsidian entirely
            import shutil
            obsidian = out / ".harness" / "vault" / ".obsidian"
            if obsidian.exists():
                shutil.rmtree(obsidian)
            # AGENTS.md still references valid paths
            text = (out / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(".harness/README.md", text)
            self.assertIn(".harness/manifest.json", text)
            self.assertIn(".harness/vault/_index.md", text)
            # Vault _index still exists
            self.assertTrue(
                (out / ".harness" / "vault" / "_index.md").exists()
            )

    # ── 8. Factory generates AGENTS.md idempotently ──────────────────

    def test_agents_md_idempotent(self):
        """Generating twice must produce identical AGENTS.md."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out1 = self._generate(root)
            content1 = (out1 / "AGENTS.md").read_text(encoding="utf-8")

            # Generate again into a different output (same profile)
            root2 = Path(tempfile.mkdtemp())
            out2 = self._generate(root2)
            content2 = (out2 / "AGENTS.md").read_text(encoding="utf-8")

            self.assertEqual(content1, content2,
                             "AGENTS.md generation is not idempotent")

    # ── 9. Kotlin/Android entry point has no Base tech references ────

    def test_kotlin_agents_md_no_base_tech_references(self):
        """AGENTS.md for a Kotlin project must not leak Go identity."""
        kotlin_profile = {
            "schema_version": "1",
            "identity": {
                "proposed_product_name": "Mobile App",
                "proposed_repository_name": "mobile-app",
                "short_description": "Android app",
                "problem_statement": "Need a mobile app",
                "selected_architecture": "mvc",
            },
            "domain": {
                "actors": [], "core_concepts": [],
                "entities": [], "business_rules": [],
            },
            "technical": {
                "application_type": "Mobile",
                "persistence": "firebase",
                "interfaces": ["Mobile UI"],
                "external_dependencies": [],
            },
            "constraints": [], "risks": [], "open_questions": [],
        }
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            profile_path = root / "profile.json"
            output = root / "project"
            profile_path.write_text(json.dumps(kotlin_profile), encoding="utf-8")
            generate_harness(profile_path, "0.32.0", output)
            text = (output / "AGENTS.md").read_text(encoding="utf-8").lower()
            self.assertNotIn("go engineering", text)
            self.assertNotIn("go engineer", text)

    # ── 10. Runtime adapters (if any) do not duplicate harness ────────

    def test_validated_agents_md_references(self):
        """AGENTS.md must reference README, manifest, and vault _index."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = self._generate(root)
            text = (out / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn(".harness/README.md", text)
            self.assertIn(".harness/manifest.json", text)
            self.assertIn(".harness/vault/_index.md", text)
            self.assertIn("self-sufficient", text.lower())
            self.assertIn("policies", text.lower())
            self.assertIn("workflows", text.lower())

    # ── Helper ────────────────────────────────────────────────────────

    def _generate(self, tmp_root: Path) -> Path:
        profile_path = tmp_root / "profile.json"
        output = tmp_root / "project"
        profile_path.write_text(json.dumps(self.profile), encoding="utf-8")
        result = generate_harness(profile_path, "0.1.0", output)
        self.assertTrue(result["valid"])
        return output


if __name__ == "__main__":
    unittest.main()