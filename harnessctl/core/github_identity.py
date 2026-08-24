from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


_GITHUB_REMOTE_RE = re.compile(
    r"(?:git@github\.com:|https?://github\.com/|ssh://git@github\.com/)"
    r"([^/]+)/([^/]+?)(?:\.git)?(?:\s|$)"
)


@dataclass
class RemoteInfo:
    name: str
    url: str
    owner: str
    repo: str


@dataclass
class PreflightResult:
    ok: bool
    root: Path
    canonical_owner: str | None = None
    canonical_repo: str | None = None
    origin: RemoteInfo | None = None
    harness_identity: dict | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "root": str(self.root),
            "canonical_owner": self.canonical_owner,
            "canonical_repo": self.canonical_repo,
            "origin": (
                {
                    "name": self.origin.name,
                    "url": self.origin.url,
                    "owner": self.origin.owner,
                    "repo": self.origin.repo,
                }
                if self.origin
                else None
            ),
            "harness_identity": self.harness_identity,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def _run_git(args: list[str], cwd: Path) -> str | None:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def _find_git_root(start: Path) -> Path | None:
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        if current.parent == current:
            return None
        current = current.parent


def _parse_github_url(url: str) -> tuple[str, str] | None:
    match = _GITHUB_REMOTE_RE.search(url.strip())
    if not match:
        return None
    owner = match.group(1)
    repo = match.group(2)
    if not owner or not repo:
        return None
    return owner, repo


def _get_remotes(root: Path) -> list[RemoteInfo]:
    output = _run_git(["remote", "-v"], root)
    if not output:
        return []
    seen: set[str] = set()
    remotes: list[RemoteInfo] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        name = parts[0]
        url = parts[1]
        key = f"{name}:{url}"
        if key in seen:
            continue
        seen.add(key)
        parsed = _parse_github_url(url)
        if parsed:
            remotes.append(
                RemoteInfo(name=name, url=url, owner=parsed[0], repo=parsed[1])
            )
    return remotes


def _get_origin(remotes: list[RemoteInfo]) -> RemoteInfo | None:
    for r in remotes:
        if r.name == "origin":
            return r
    return None


def _load_harness_identity(root: Path) -> dict | None:
    manifest_path = root / ".harness" / "manifest.json"
    if not manifest_path.exists():
        return None
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    identity = data.get("confirmed_github_identity")
    if isinstance(identity, dict) and identity.get("owner") and identity.get("repo"):
        return identity
    return None


def _record_harness_identity(root: Path, owner: str, repo: str) -> bool:
    manifest_path = root / ".harness" / "manifest.json"
    if not manifest_path.exists():
        return False
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    data["confirmed_github_identity"] = {"owner": owner, "repo": repo}
    manifest_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    return True


def preflight_github(
    start: Path,
    *,
    expected_owner: str | None = None,
    expected_repo: str | None = None,
    record: bool = False,
) -> PreflightResult:
    root = _find_git_root(start)
    if root is None:
        return PreflightResult(
            ok=False,
            root=start.resolve(),
            errors=["Not inside a Git repository."],
        )

    result = PreflightResult(ok=True, root=root)

    remotes = _get_remotes(root)
    origin = _get_origin(remotes)
    result.origin = origin

    if origin is None:
        result.ok = False
        result.errors.append(
            "No GitHub 'origin' remote found. "
            "Cannot infer repository identity from local path."
        )
        return result

    harness_identity = _load_harness_identity(root)
    result.harness_identity = harness_identity

    candidates: list[tuple[str, str, str]] = []
    candidates.append(("origin", origin.owner, origin.repo))

    if harness_identity:
        candidates.append(
            ("harness", harness_identity["owner"], harness_identity["repo"])
        )

    if expected_owner and expected_repo:
        candidates.append(("explicit", expected_owner, expected_repo))

    canonical_owner = candidates[0][1]
    canonical_repo = candidates[0][2]

    for source, owner, repo in candidates[1:]:
        if owner != canonical_owner or repo != canonical_repo:
            result.ok = False
            result.errors.append(
                f"GitHub identity divergence: '{source}' says "
                f"{owner}/{repo} but 'origin' says "
                f"{canonical_owner}/{canonical_repo}. "
                "Halting: will not guess."
            )
            return result

    result.canonical_owner = canonical_owner
    result.canonical_repo = canonical_repo

    if not harness_identity and record:
        recorded = _record_harness_identity(root, canonical_owner, canonical_repo)
        if recorded:
            result.harness_identity = {
                "owner": canonical_owner,
                "repo": canonical_repo,
            }
            result.warnings.append(
                f"Recorded canonical identity {canonical_owner}/{canonical_repo} "
                "in .harness/manifest.json."
            )
        else:
            result.warnings.append(
                "Could not record identity: .harness/manifest.json not found "
                "or not writable. Continuing with origin-confirmed identity."
            )

    return result


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="github-identity-preflight",
        description=(
            "Resolve and validate the GitHub repository identity from trusted "
            "sources before any GitHub operation. Never infers from local path."
        ),
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Directory to check (defaults to current directory).",
    )
    parser.add_argument("--owner", help="Explicit expected owner/login.")
    parser.add_argument("--repo", help="Explicit expected repository name.")
    parser.add_argument(
        "--record",
        action="store_true",
        help="Record the confirmed identity in .harness/manifest.json.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="json",
    )
    args = parser.parse_args()

    result = preflight_github(
        args.path,
        expected_owner=args.owner,
        expected_repo=args.repo,
        record=args.record,
    )

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        if result.ok:
            print(f"OK: {result.canonical_owner}/{result.canonical_repo}")
            if result.origin:
                print(f"  origin: {result.origin.url}")
            if result.harness_identity:
                print("  harness: identity recorded")
        else:
            for err in result.errors:
                print(f"ERROR: {err}", file=sys.stderr)
            for warn in result.warnings:
                print(f"WARN: {warn}", file=sys.stderr)

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
