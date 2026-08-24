from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


_BRANCH_RE = re.compile(r"^(main|develop|feature/.+|story/.+|hotfix/.+)$")
_FEATURE_RE = re.compile(r"^feature/(.+)$")
_STORY_RE = re.compile(r"^story/(.+)$")
_HOTFIX_RE = re.compile(r"^hotfix/(.+)$")


@dataclass
class BranchInfo:
    name: str
    parent: str | None
    branch_type: str


@dataclass
class BranchCheckResult:
    ok: bool
    root: Path
    current_branch: str | None = None
    branch_type: str | None = None
    expected_parent: str | None = None
    actual_parent: str | None = None
    main_exists: bool = False
    develop_exists: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "root": str(self.root),
            "current_branch": self.current_branch,
            "branch_type": self.branch_type,
            "expected_parent": self.expected_parent,
            "actual_parent": self.actual_parent,
            "main_exists": self.main_exists,
            "develop_exists": self.develop_exists,
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


def _get_current_branch(root: Path) -> str | None:
    output = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], root)
    if not output or output == "HEAD":
        return None
    return output


def _branch_exists(root: Path, branch: str) -> bool:
    output = _run_git(
        ["rev-parse", "--verify", "--quiet", branch], root
    )
    return output is not None and output != ""


def _get_merge_base(root: Path, branch_a: str, branch_b: str) -> str | None:
    return _run_git(["merge-base", branch_a, branch_b], root)


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    output = _run_git(
        ["merge-base", "--is-ancestor", ancestor, descendant], root
    )
    return output is not None and output == ""


def _classify_branch(branch: str) -> str:
    if branch in ("main", "master"):
        return "main"
    if branch == "develop":
        return "develop"
    if _FEATURE_RE.match(branch):
        return "feature"
    if _STORY_RE.match(branch):
        return "story"
    if _HOTFIX_RE.match(branch):
        return "hotfix"
    return "unknown"


def _validate_branch_name(branch: str) -> bool:
    return bool(_BRANCH_RE.match(branch))


def _get_branch_parent(root: Path, branch: str) -> str | None:
    output = _run_git(
        ["rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}"], root
    )
    if output and output != branch:
        return output
    return None


def check_branch(
    start: Path,
    *,
    expected_branch: str | None = None,
) -> BranchCheckResult:
    root = _find_git_root(start)
    if root is None:
        return BranchCheckResult(
            ok=False,
            root=start.resolve(),
            errors=["Not inside a Git repository."],
        )

    result = BranchCheckResult(ok=True, root=root)

    main_exists = _branch_exists(root, "main") or _branch_exists(root, "master")
    develop_exists = _branch_exists(root, "develop")
    result.main_exists = main_exists
    result.develop_exists = develop_exists

    if not main_exists:
        result.errors.append(
            "Required branch 'main' does not exist. "
            "Create it before any feature/develop work."
        )
        result.ok = False

    current = _get_current_branch(root)
    result.current_branch = current

    if expected_branch and current != expected_branch:
        result.errors.append(
            f"Expected branch '{expected_branch}' but current branch is "
            f"'{current}'. Switch before proceeding."
        )
        result.ok = False

    if current is None:
        result.errors.append(
            "Detached HEAD state. Checkout a valid branch before proceeding."
        )
        result.ok = False
        return result

    branch_type = _classify_branch(current)
    result.branch_type = branch_type

    if branch_type == "unknown":
        result.errors.append(
            f"Branch '{current}' does not match the branching model. "
            "Allowed: main, develop, feature/<name>, story/<name>, hotfix/<name>."
        )
        result.ok = False
        return result

    if not _validate_branch_name(current):
        result.errors.append(
            f"Branch name '{current}' is invalid. "
            "Use kebab-case after the prefix (e.g., feature/my-feature)."
        )
        result.ok = False

    if branch_type == "main":
        result.warnings.append(
            "On 'main'. Direct commits are prohibited. "
            "Work should happen on feature/story branches."
        )
        return result

    if branch_type == "develop":
        result.warnings.append(
            "On 'develop'. Direct commits are discouraged. "
            "Work should happen on feature/story branches."
        )
        return result

    if branch_type == "feature":
        if not develop_exists:
            result.errors.append(
                "Feature branch created but 'develop' does not exist. "
                "Feature branches must be created from 'develop'."
            )
            result.ok = False
        else:
            result.expected_parent = "develop"
            if _is_ancestor(root, "develop", current):
                result.actual_parent = "develop"
            else:
                result.actual_parent = None
                result.errors.append(
                    f"Feature branch '{current}' does not appear to be based on "
                    "'develop'. Feature branches must branch from 'develop'."
                )
                result.ok = False

    if branch_type == "story":
        feature_branch = None
        story_name = _STORY_RE.match(current)
        if story_name:
            pass
        parent = _get_branch_parent(root, current)
        result.actual_parent = parent
        if parent and _FEATURE_RE.match(parent):
            result.expected_parent = parent
        else:
            result.expected_parent = "feature/<parent>"
            result.errors.append(
                f"Story branch '{current}' must be based on a 'feature/' branch. "
                f"Actual upstream: {parent or 'none'}. "
                "Story branches branch from their parent feature branch."
            )
            result.ok = False

    if branch_type == "hotfix":
        if not main_exists:
            result.errors.append(
                "Hotfix branch created but 'main' does not exist. "
                "Hotfix branches must be created from 'main'."
            )
            result.ok = False
        else:
            result.expected_parent = "main"
            if _is_ancestor(root, "main", current) or _is_ancestor(root, "master", current):
                result.actual_parent = "main"
            else:
                result.actual_parent = None
                result.errors.append(
                    f"Hotfix branch '{current}' does not appear to be based on "
                    "'main'. Hotfix branches branch from 'main'."
                )
                result.ok = False

    return result


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="branch-check",
        description=(
            "Validate the current Git branch against the mandatory branching model. "
            "Checks branch name, parent lineage, and model conformance."
        ),
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Directory to check (defaults to current directory).",
    )
    parser.add_argument(
        "--branch",
        help="Explicit expected current branch name.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="json",
    )
    args = parser.parse_args()

    result = check_branch(args.path, expected_branch=args.branch)

    if args.format == "json":
        print(_result_to_json(result))
    else:
        if result.ok:
            print(f"OK: branch '{result.current_branch}' ({result.branch_type})")
            if result.expected_parent:
                print(f"  expected parent: {result.expected_parent}")
            if result.actual_parent:
                print(f"  actual parent: {result.actual_parent}")
        else:
            for err in result.errors:
                print(f"ERROR: {err}", file=sys.stderr)
        for warn in result.warnings:
            print(f"WARN: {warn}", file=sys.stderr)

    return 0 if result.ok else 1


def _result_to_json(result: BranchCheckResult) -> str:
    import json

    return json.dumps(result.to_dict(), indent=2)


if __name__ == "__main__":
    raise SystemExit(main())
