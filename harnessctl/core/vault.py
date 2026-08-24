from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

import yaml


_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_WIKILINK_RE = re.compile(r"\[\[([^|#]+?)(?:\|([^]]+?))?\]\]")
_CANONICAL_REF_RE = re.compile(r"\[\[docs/([^]]+)\]\]")


@dataclass
class VaultNote:
    id: str
    type: str
    title: str
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    related: list[dict] = field(default_factory=list)
    canonical_doc: str | None = None
    body: str = ""
    links_to: list[str] = field(default_factory=list)
    linked_from: list[str] = field(default_factory=list)
    filepath: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _parse_frontmatter(text: str) -> dict:
    match = _FM_RE.match(text)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _strip_frontmatter(text: str) -> str:
    return _FM_RE.sub("", text, count=1).strip()


def _extract_title(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line.lstrip("# ")
    return ""


def _resolve_wikilink_target(target: str) -> str:
    target = target.strip()
    if target.startswith("docs/"):
        return target
    return target


def load_vault(vault_root: Path) -> dict[str, VaultNote]:
    notes: dict[str, VaultNote] = {}
    if not vault_root.exists():
        return notes

    for fpath in sorted(vault_root.rglob("*.md")):
        text = fpath.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if not fm:
            continue
        body = _strip_frontmatter(text)
        note_id = fm.get("id", fpath.stem)
        title = fm.get("title", _extract_title(body) or fpath.stem)
        links_to = []
        for match in _WIKILINK_RE.finditer(body):
            target = _resolve_wikilink_target(match.group(1))
            links_to.append(target)

        note = VaultNote(
            id=note_id,
            type=fm.get("type", "unknown"),
            title=title,
            aliases=fm.get("aliases", []),
            tags=fm.get("tags", []),
            related=fm.get("related", []),
            canonical_doc=fm.get("canonical_doc"),
            body=body,
            links_to=list(set(links_to)),
            filepath=str(fpath.relative_to(vault_root)),
        )
        notes[note_id] = note

    for note_id, note in notes.items():
        for target_id in note.links_to:
            target = notes.get(target_id)
            if target:
                target.linked_from.append(note_id)

    return notes


def query_notes(
    notes: dict[str, VaultNote],
    find: str | None = None,
    follow: str | None = None,
    graph: bool = False,
) -> dict:
    if find:
        term = find.lower()
        results = []
        for note in notes.values():
            if term in note.id.lower() or term in note.title.lower():
                results.append(note.to_dict())
                continue
            if any(term in a.lower() for a in note.aliases):
                results.append(note.to_dict())
                continue
            if any(term in t.lower() for t in note.tags):
                results.append(note.to_dict())
                continue
            if term in note.body.lower():
                results.append(note.to_dict())
                continue
        return {"ok": True, "action": "find", "term": find, "results": results}

    if follow:
        note = notes.get(follow)
        if not note:
            return {"ok": False, "error": f"Note not found: {follow}"}
        links = [notes.get(t) for t in note.links_to if t in notes]
        backlinks = [notes.get(s) for s in note.linked_from if s in notes]
        return {
            "ok": True,
            "action": "follow",
            "note": note.to_dict(),
            "links_to": [n.to_dict() for n in links if n],
            "linked_from": [n.to_dict() for n in backlinks if n],
        }

    return {"ok": False, "error": "Specify --find or --follow"}


def graph_summary(notes: dict[str, VaultNote]) -> dict:
    edges = []
    for note_id, note in notes.items():
        for link in note.links_to:
            edges.append({"from": note_id, "to": link})
    return {
        "ok": True,
        "nodes": len(notes),
        "edges": len(edges),
        "node_list": sorted(notes.keys()),
        "edges_list": edges,
    }


def validate_vault(notes: dict[str, VaultNote], vault_root: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []

    for note_id, note in notes.items():
        if not note_id:
            issues.append(f"Note {note.filepath}: missing 'id' in frontmatter")
        if note.type == "unknown":
            issues.append(f"Note {note.filepath}: missing or invalid 'type'")
        for link in note.links_to:
            if link.startswith("docs/"):
                doc_path = vault_root.parent / link
                if not doc_path.exists():
                    warnings.append(
                        f"Note {note.filepath}: canonical doc '{link}' not found"
                    )
            elif link not in notes and link != note_id:
                warnings.append(
                    f"Note {note.filepath}: wikilink '[[{link}]]' target not in vault"
                )
        for rel in note.related:
            rel_id = rel.get("id") if isinstance(rel, dict) else None
            if rel_id and rel_id not in notes and rel_id != "_index":
                warnings.append(
                    f"Note {note.filepath}: related note '{rel_id}' not in vault"
                )
        if note.canonical_doc and note.canonical_doc.startswith("docs/"):
            doc_path = vault_root.parent / note.canonical_doc
            if not doc_path.exists():
                warnings.append(
                    f"Note {note.filepath}: canonical_doc '{note.canonical_doc}' not found"
                )

    return {
        "valid": len(issues) == 0,
        "total_notes": len(notes),
        "issues": issues,
        "warnings": warnings,
    }


def _copy_obsidian_config(src_vault: Path, dst_vault: Path) -> None:
    obsidian_src = src_vault / ".obsidian"
    if not obsidian_src.exists():
        return
    obsidian_dst = dst_vault / ".obsidian"
    obsidian_dst.mkdir(parents=True, exist_ok=True)
    for fname in ["app.json", "core-plugins.json", "community-plugins.json", "appearance.json", ".gitignore"]:
        src_file = obsidian_src / fname
        if src_file.exists():
            content = src_file.read_text(encoding="utf-8")
            (obsidian_dst / fname).write_text(content, encoding="utf-8")


def materialize_vault(
    base_root: Path,
    dedicated_root: Path,
    selected_ids: list[str] | None = None,
    base_version: str = "unknown",
) -> dict:
    vault_root = base_root / "vault"
    notes = load_vault(vault_root)
    if not notes:
        return {"ok": False, "error": "Base vault not found"}

    if selected_ids:
        note_ids = [nid for nid in selected_ids if nid in notes]
    else:
        note_ids = list(notes.keys())

    out_vault = dedicated_root / ".harness" / "vault"
    out_vault.mkdir(parents=True, exist_ok=True)

    copied = []
    for note_id in note_ids:
        note = notes[note_id]
        src = vault_root / note.filepath
        content = src.read_text(encoding="utf-8")
        content = _CANONICAL_REF_RE.sub(r"[[\1]]", content)
        dest = out_vault / note.filepath
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        copied.append(note_id)

    manifest = {
        "base_version": base_version,
        "generated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "note_count": len(copied),
        "note_ids": copied,
    }
    (out_vault / "vault-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    # Copy Obsidian configuration
    _copy_obsidian_config(vault_root, out_vault)

    return {
        "ok": True,
        "copied_notes": len(copied),
        "note_ids": copied,
        "output": str(out_vault),
    }