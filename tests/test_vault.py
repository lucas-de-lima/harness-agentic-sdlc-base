from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harnessctl.core.vault import (
    load_vault,
    query_notes,
    graph_summary,
    validate_vault,
    materialize_vault,
    _parse_frontmatter,
    _strip_frontmatter,
    _WIKILINK_RE,
    _CANONICAL_REF_RE,
)

OBSIDIAN_APP = '{"alwaysUpdateLinks": true, "attachmentFolderPath": "./", "newFileLocation": "current"}'
OBSIDIAN_CORE = '["file-explorer", "search", "graph", "backlinks"]'
OBSIDIAN_COMMUNITY = "[]"
OBSIDIAN_APPEARANCE = '{"theme": "obsidian"}'
OBSIDIAN_GITIGNORE = "workspace\nworkspace.json\nworkspace-mobile\ncache/\nplugins/\n"


SAMPLE_NOTE = """\
---
id: test-note
type: domain
tags: [test]
aliases: [test-alias]
related:
  - id: _index
    relation: part_of
canonical_doc: docs/SOME_DOC.md
---

# Test Note

Content with [[governance|link to governance]] and [[docs/OTHER_DOC.md]].
"""

SAMPLE_INDEX = """\
---
id: _index
type: root
aliases: [home]
tags: [vault]
---

# Index

Links to [[test-note]] and [[missing-note]].
"""

SAMPLE_SECOND = """\
---
id: governance
type: domain
aliases: [gov]
tags: [governance]
---

# Governance

Linked from [[test-note]].
"""


class FrontmatterTests(unittest.TestCase):
    def test_parse_valid_frontmatter(self):
        fm = _parse_frontmatter(SAMPLE_NOTE)
        self.assertEqual(fm["id"], "test-note")
        self.assertEqual(fm["type"], "domain")
        self.assertEqual(fm["tags"], ["test"])

    def test_parse_no_frontmatter(self):
        fm = _parse_frontmatter("# Just a title\n\nSome text.")
        self.assertEqual(fm, {})

    def test_strip_frontmatter(self):
        body = _strip_frontmatter(SAMPLE_NOTE)
        self.assertTrue(body.startswith("# Test Note"))
        self.assertNotIn("---", body[:5])

    def test_wikilink_regex(self):
        matches = _WIKILINK_RE.findall("before [[governance]] after [[docs/X.md|alias]]")
        self.assertEqual(matches[0][0], "governance")
        self.assertEqual(matches[1][0], "docs/X.md")
        self.assertEqual(matches[1][1], "alias")

    def test_canonical_ref_regex(self):
        matches = _CANONICAL_REF_RE.findall("[[docs/HARNESS_BASE_CONSTITUTION.md]]")
        self.assertEqual(matches[0], "HARNESS_BASE_CONSTITUTION.md")


class VaultLoadingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        v = self.tmp / "vault"
        v.mkdir()
        (v / "_index.md").write_text(SAMPLE_INDEX, encoding="utf-8")
        (v / "test-note.md").write_text(SAMPLE_NOTE, encoding="utf-8")
        (v / "governance.md").write_text(SAMPLE_SECOND, encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_load_vault_returns_notes_by_id(self):
        notes = load_vault(self.tmp / "vault")
        self.assertIn("_index", notes)
        self.assertIn("test-note", notes)
        self.assertIn("governance", notes)
        self.assertEqual(len(notes), 3)

    def test_load_vault_empty_if_no_vault(self):
        notes = load_vault(self.tmp / "nonexistent")
        self.assertEqual(notes, {})

    def test_notes_have_backlinks(self):
        notes = load_vault(self.tmp / "vault")
        gov = notes["governance"]
        self.assertIn("test-note", gov.linked_from)

    def test_links_to_outside_vault_logged(self):
        notes = load_vault(self.tmp / "vault")
        tn = notes["test-note"]
        self.assertIn("docs/OTHER_DOC.md", tn.links_to)


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        v = self.tmp / "vault"
        v.mkdir()
        (v / "_index.md").write_text(SAMPLE_INDEX, encoding="utf-8")
        (v / "test-note.md").write_text(SAMPLE_NOTE, encoding="utf-8")
        (v / "governance.md").write_text(SAMPLE_SECOND, encoding="utf-8")
        self.notes = load_vault(v)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_find_by_id(self):
        r = query_notes(self.notes, find="governance")
        self.assertTrue(r["ok"])
        # matches id and body of test-note which links to [[governance]]
        self.assertGreaterEqual(len(r["results"]), 1)
        self.assertEqual(r["results"][0]["id"], "governance")

    def test_find_by_alias(self):
        r = query_notes(self.notes, find="test-alias")
        self.assertTrue(r["ok"])
        self.assertEqual(len(r["results"]), 1)

    def test_find_by_tag(self):
        r = query_notes(self.notes, find="test")
        self.assertTrue(r["ok"])
        self.assertGreaterEqual(len(r["results"]), 1)

    def test_find_no_match(self):
        r = query_notes(self.notes, find="zzzznotfound")
        self.assertTrue(r["ok"])
        self.assertEqual(len(r["results"]), 0)

    def test_follow_note(self):
        r = query_notes(self.notes, follow="test-note")
        self.assertTrue(r["ok"])
        self.assertEqual(r["note"]["id"], "test-note")
        self.assertGreater(len(r["links_to"]), 0)

    def test_follow_nonexistent(self):
        r = query_notes(self.notes, follow="nonexistent")
        self.assertFalse(r["ok"])

    def test_graph_summary(self):
        r = graph_summary(self.notes)
        self.assertTrue(r["ok"])
        self.assertEqual(r["nodes"], 3)
        self.assertGreaterEqual(r["edges"], 2)


class ValidateVaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        v = self.tmp / "vault"
        v.mkdir()
        (v / "_index.md").write_text(SAMPLE_INDEX, encoding="utf-8")
        (v / "test-note.md").write_text(SAMPLE_NOTE, encoding="utf-8")
        (v / "governance.md").write_text(SAMPLE_SECOND, encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_valid_vault_has_no_issues(self):
        notes = load_vault(vault_root=self.tmp / "vault")
        r = validate_vault(notes, self.tmp / "vault")
        self.assertTrue(r["valid"])
        self.assertEqual(len(r["issues"]), 0)

    def test_notes_without_frontmatter_are_skipped(self):
        v = self.tmp / "vault"
        (v / "no-fm.md").write_text("# No frontmatter\n\nJust text.", encoding="utf-8")
        notes = load_vault(v)
        r = validate_vault(notes, v)
        # no-fm.md was skipped because no frontmatter → not in notes
        self.assertEqual(len(notes), 3)

    def test_warns_on_missing_wikilink_targets(self):
        notes = load_vault(self.tmp / "vault")
        # _index links to [[missing-note]] which doesn't exist
        r = validate_vault(notes, self.tmp / "vault")
        # should have a warning about missing-note
        missing_warnings = [w for w in r["warnings"] if "missing-note" in w]
        self.assertGreaterEqual(len(missing_warnings), 1)

    def test_warns_on_missing_canonical_doc(self):
        notes = load_vault(self.tmp / "vault")
        # test-note links to docs/SOME_DOC.md which does not exist
        r = validate_vault(notes, self.tmp / "vault")
        doc_warnings = [w for w in r["warnings"] if "SOME_DOC.md" in w]
        self.assertGreaterEqual(len(doc_warnings), 1)


class MaterializeTests(unittest.TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.dedicated = Path(tempfile.mkdtemp())
        v = self.base / "vault"
        v.mkdir()
        (v / "_index.md").write_text(SAMPLE_INDEX, encoding="utf-8")
        (v / "test-note.md").write_text(SAMPLE_NOTE, encoding="utf-8")
        (v / "governance.md").write_text(SAMPLE_SECOND, encoding="utf-8")
        self._add_obsidian_config(v)

    @staticmethod
    def _add_obsidian_config(vault: Path) -> None:
        obsidian = vault / ".obsidian"
        obsidian.mkdir(parents=True, exist_ok=True)
        (obsidian / "app.json").write_text(OBSIDIAN_APP, encoding="utf-8")
        (obsidian / "core-plugins.json").write_text(OBSIDIAN_CORE, encoding="utf-8")
        (obsidian / "community-plugins.json").write_text(OBSIDIAN_COMMUNITY, encoding="utf-8")
        (obsidian / "appearance.json").write_text(OBSIDIAN_APPEARANCE, encoding="utf-8")
        (obsidian / ".gitignore").write_text(OBSIDIAN_GITIGNORE, encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.rmtree(self.dedicated, ignore_errors=True)

    def test_materialize_all_notes(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        self.assertEqual(r["copied_notes"], 3)
        self.assertTrue((self.dedicated / ".harness" / "vault" / "_index.md").exists())
        self.assertTrue(
            (self.dedicated / ".harness" / "vault" / "vault-manifest.json").exists()
        )

    def test_materialize_selected_ids(self):
        r = materialize_vault(
            self.base, self.dedicated, selected_ids=["governance"], base_version="0.30.0"
        )
        self.assertTrue(r["ok"])
        self.assertEqual(r["copied_notes"], 1)
        self.assertEqual(r["note_ids"], ["governance"])

    def test_materialize_rewrites_docs_links(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        content = (
            self.dedicated / ".harness" / "vault" / "test-note.md"
        ).read_text(encoding="utf-8")
        # [[docs/OTHER_DOC.md]] should become [[OTHER_DOC.md]]
        self.assertIn("[[OTHER_DOC.md]]", content)
        # vault-to-vault wikilinks preserved
        self.assertIn("[[governance", content)

    def test_materialize_manifest_has_base_version(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        manifest_path = self.dedicated / ".harness" / "vault" / "vault-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["base_version"], "0.30.0")
        self.assertEqual(manifest["note_count"], 3)

    def test_portability_no_base(self):
        """Dedicated vault must function without Base being present."""
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])

        # Simulate clone without Base
        import shutil
        shutil.rmtree(self.base, ignore_errors=True)

        # Must load and validate the dedicated vault independently
        dedicated_vault = self.dedicated / ".harness" / "vault"
        self.assertTrue(dedicated_vault.exists())
        notes = load_vault(dedicated_vault)
        self.assertGreaterEqual(len(notes), 1)

        # Validate: no external link issues are blocking
        r = validate_vault(notes, dedicated_vault)
        # Some warnings about missing docs/ references are acceptable
        # But no hard issues (missing id, type)
        self.assertTrue(r["valid"])


class ObsidianConfigTests(unittest.TestCase):
    """Tests for the minimal, portable Obsidian configuration."""

    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        self.dedicated = Path(tempfile.mkdtemp())
        v = self.base / "vault"
        v.mkdir()
        (v / "_index.md").write_text(SAMPLE_INDEX, encoding="utf-8")
        (v / "test-note.md").write_text(SAMPLE_NOTE, encoding="utf-8")
        (v / "governance.md").write_text(SAMPLE_SECOND, encoding="utf-8")
        MaterializeTests._add_obsidian_config(v)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.base, ignore_errors=True)
        shutil.rmtree(self.dedicated, ignore_errors=True)

    def test_1_obsidian_created_in_dedicated(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        obsidian = self.dedicated / ".harness" / "vault" / ".obsidian"
        self.assertTrue(obsidian.exists())
        self.assertTrue((obsidian / "app.json").exists())
        self.assertTrue((obsidian / "core-plugins.json").exists())
        self.assertTrue((obsidian / "community-plugins.json").exists())
        self.assertTrue((obsidian / "appearance.json").exists())
        self.assertTrue((obsidian / ".gitignore").exists())

    def test_2_config_has_no_absolute_paths(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        obsidian = self.dedicated / ".harness" / "vault" / ".obsidian"
        for f in obsidian.iterdir():
            if f.suffix == ".json":
                content = f.read_text(encoding="utf-8")
                self.assertNotIn(str(self.base), content)
                self.assertNotIn(":/", content)
                self.assertNotIn("\\\\", content)

    def test_3_no_community_plugins_required(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        cp = self.dedicated / ".harness" / "vault" / ".obsidian" / "community-plugins.json"
        plugins = json.loads(cp.read_text(encoding="utf-8"))
        self.assertEqual(plugins, [])

    def test_4_vault_valid_without_obsidian(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        dedicated_vault = self.dedicated / ".harness" / "vault"

        # Remove .obsidian entirely
        import shutil
        shutil.rmtree(dedicated_vault / ".obsidian", ignore_errors=True)

        notes = load_vault(dedicated_vault)
        self.assertGreaterEqual(len(notes), 1)
        vr = validate_vault(notes, dedicated_vault)
        self.assertTrue(vr["valid"])

    def test_4b_obsidian_contains_only_config_no_knowledge(self):
        """Regression guard: .obsidian must never contain knowledge files."""
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        obsidian = self.dedicated / ".harness" / "vault" / ".obsidian"
        # Verify zero markdown, yaml, or yml files inside .obsidian
        md_files = list(obsidian.rglob("*.md"))
        yaml_files = list(obsidian.rglob("*.yaml")) + list(obsidian.rglob("*.yml"))
        self.assertEqual(md_files, [], f"Markdown files found inside .obsidian: {md_files}")
        self.assertEqual(yaml_files, [], f"YAML files found inside .obsidian: {yaml_files}")
        # Only allowed file: known config files
        allowed = {"app.json", "core-plugins.json", "community-plugins.json", "appearance.json", ".gitignore"}
        for item in obsidian.iterdir():
            if item.is_dir():
                continue
            self.assertIn(item.name, allowed,
                          f"Unexpected file inside .obsidian: {item.name}")

    def test_5_base_has_own_minimal_config(self):
        notes = load_vault(self.base / "vault")
        self.assertGreaterEqual(len(notes), 1)
        obsidian = self.base / "vault" / ".obsidian"
        self.assertTrue(obsidian.exists())
        self.assertTrue((obsidian / "app.json").exists())
        self.assertTrue((obsidian / "core-plugins.json").exists())
        self.assertTrue((obsidian / "community-plugins.json").exists())
        # Core graph/backlinks enabled
        core = json.loads((obsidian / "core-plugins.json").read_text(encoding="utf-8"))
        self.assertIn("graph", core)
        self.assertIn("backlinks", core)

    def test_6_materialization_reproduces_config(self):
        r = materialize_vault(self.base, self.dedicated, base_version="0.30.0")
        self.assertTrue(r["ok"])
        src = self.base / "vault" / ".obsidian"
        dst = self.dedicated / ".harness" / "vault" / ".obsidian"
        for fname in ["app.json", "core-plugins.json", "community-plugins.json", "appearance.json", ".gitignore"]:
            self.assertEqual(
                (dst / fname).read_text(encoding="utf-8"),
                (src / fname).read_text(encoding="utf-8"),
                f"Config file {fname} not reproduced correctly",
            )


class RealVaultTests(unittest.TestCase):
    """Tests against the actual Base vault to ensure it's well-formed."""

    def setUp(self):
        self.base_root = Path(__file__).resolve().parents[1]
        self.vault_root = self.base_root / "vault"

    def test_real_vault_loads(self):
        notes = load_vault(self.vault_root)
        self.assertGreaterEqual(len(notes), 7)  # at least 7 notes

    def test_real_vault_has_index(self):
        notes = load_vault(self.vault_root)
        self.assertIn("_index", notes)

    def test_real_vault_all_notes_have_id_and_type(self):
        notes = load_vault(self.vault_root)
        for note_id, note in notes.items():
            self.assertTrue(note_id, f"{note.filepath}: missing id")
            self.assertNotEqual(note.type, "unknown", f"{note.filepath}: missing type")

    def test_real_vault_graph_has_edges(self):
        notes = load_vault(self.vault_root)
        r = graph_summary(notes)
        self.assertGreater(r["edges"], 5)

    def test_real_vault_observable_notes(self):
        notes = load_vault(self.vault_root)
        expected_ids = {"_index", "governance", "architecture", "agents", "skills", "workflows", "policies", "tools"}
        found_ids = set(notes.keys())
        self.assertTrue(expected_ids.issubset(found_ids),
                        f"Missing notes: {expected_ids - found_ids}")

    def test_real_vault_all_canonical_links_resolve(self):
        notes = load_vault(self.vault_root)
        for note_id, note in notes.items():
            for link in note.links_to:
                if link.startswith("docs/"):
                    doc_path = self.base_root / link
                    self.assertTrue(
                        doc_path.exists(),
                        f"{note.filepath}: canonical doc '{link}' not found at {doc_path}"
                    )

    def test_real_base_has_obsidian_config(self):
        obsidian = self.vault_root / ".obsidian"
        self.assertTrue(obsidian.exists())
        for fname in ["app.json", "core-plugins.json", "community-plugins.json", "appearance.json", ".gitignore"]:
            self.assertTrue((obsidian / fname).exists(), f"missing .obsidian/{fname}")
        # No absolute paths in the Base obsidian config
        for f in obsidian.iterdir():
            if f.suffix == ".json":
                content = f.read_text(encoding="utf-8")
                self.assertNotIn(":/", content)
        # Community plugins empty (optional requirement)
        cp = json.loads((obsidian / "community-plugins.json").read_text(encoding="utf-8"))
        self.assertEqual(cp, [])
        # No knowledge files inside .obsidian
        self.assertEqual(list(obsidian.rglob("*.md")), [],
                         "Base .obsidian contains markdown files — must only have config")
        self.assertEqual(list(obsidian.rglob("*.yaml")) + list(obsidian.rglob("*.yml")), [],
                         "Base .obsidian contains YAML files — must only have config")