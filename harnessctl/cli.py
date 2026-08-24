from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core.factory import generate_harness
from .core.validator import validate_base, validate_dedicated
from .core.github_identity import preflight_github
from .core.gitignore import generate_gitignore, validate_gitignore, supported_languages
from .core.branching import check_branch
from .core.hitl import (
    create_gate,
    approve_gate,
    reject_gate,
    resume_check,
    list_gates,
    check_merge_allowed,
    validate_dedicated_hitl,
    reconcile_gate,
    record_manual_merge,
    MANDATORY_GATES,
    MERGE_ORIGINS,
    PR_STATES,
)
from .core.vault import (
    load_vault,
    query_notes,
    graph_summary,
    validate_vault,
    materialize_vault,
)
from .core.merge import controlled_merge, MERGE_TYPE_MAP


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harnessctl",
        description="Agentic SDLC Base Harness tooling.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate a Base or Dedicated Harness.")
    validate.add_argument("path", type=Path)
    validate.add_argument(
        "--kind",
        choices=("base", "dedicated"),
        required=True,
    )

    generate = sub.add_parser(
        "generate",
        help="Generate a Dedicated Harness from a Project Profile.",
    )
    generate.add_argument("--profile", type=Path, required=True)
    generate.add_argument("--base-version", required=True)
    generate.add_argument("--output", type=Path, required=True)

    show_version = sub.add_parser("version", help="Show harnessctl version.")

    preflight = sub.add_parser(
        "preflight",
        help=(
            "Resolve and validate the GitHub repository identity from trusted "
            "sources (git root, origin remote, harness manifest). Never infers "
            "from local path. Run before any GitHub operation."
        ),
    )
    preflight.add_argument("--path", type=Path, default=Path("."), help="Directory to check.")
    preflight.add_argument("--owner", help="Explicit expected owner/login.")
    preflight.add_argument("--repo", help="Explicit expected repository name.")
    preflight.add_argument(
        "--record",
        action="store_true",
        help="Record the confirmed identity in .harness/manifest.json.",
    )

    gitignore = sub.add_parser(
        "gitignore",
        help="Generate or validate a stack-appropriate .gitignore.",
    )
    gitignore.add_argument("path", type=Path, help="Project root directory.")
    gitignore.add_argument(
        "--language",
        required=True,
        help=f"Language/stack ({', '.join(supported_languages())}).",
    )
    gitignore.add_argument(
        "--check",
        action="store_true",
        help="Validate only; do not create or modify files.",
    )

    branch_check = sub.add_parser(
        "branch-check",
        help=(
            "Validate the current Git branch against the mandatory branching model "
            "(main, develop, feature/, story/, hotfix/). Run before starting "
            "implementation work."
        ),
    )
    branch_check.add_argument(
        "--path",
        type=Path,
        default=Path("."),
        help="Directory to check.",
    )
    branch_check.add_argument(
        "--branch",
        help="Explicit expected current branch name.",
    )

    # --- HITL ---
    hitl = sub.add_parser(
        "hitl",
        help="Human-in-the-Loop gate management: create, approve, reject, resume, list.",
    )
    hitl_sub = hitl.add_subparsers(dest="hitl_command", required=True)

    hitl_gate = hitl_sub.add_parser("gate", help="Create a pending Human Gate (agent calls this).")
    hitl_gate.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_gate.add_argument("--gate-id", required=True, choices=sorted(MANDATORY_GATES))
    hitl_gate.add_argument("--workflow", required=True, help="Workflow ID (e.g., WF-005).")
    hitl_gate.add_argument("--object", required=True, help="Affected object (branch/feature/story).")
    hitl_gate.add_argument("--reason", required=True, help="Why the gate is required.")
    hitl_gate.add_argument("--evidence", required=True, help="Supporting evidence summary.")
    hitl_gate.add_argument("--authority", required=True, help="Expected approver role.")

    hitl_approve = hitl_sub.add_parser("approve", help="Approve a Human Gate (human calls this).")
    hitl_approve.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_approve.add_argument("--id", required=True, help="Gate instance ID.")
    hitl_approve.add_argument("--by", required=True, help="Human approver identity.")
    hitl_approve.add_argument("--note", help="Optional observation.")
    hitl_approve.add_argument(
        "--merge-origin",
        choices=sorted(MERGE_ORIGINS),
        help="How the merge was/will be executed (human_manual or harness_controlled).",
    )

    hitl_reject = hitl_sub.add_parser("reject", help="Reject a Human Gate (human calls this).")
    hitl_reject.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_reject.add_argument("--id", required=True, help="Gate instance ID.")
    hitl_reject.add_argument("--by", required=True, help="Human rejecter identity.")
    hitl_reject.add_argument("--note", help="Optional observation.")

    hitl_resume = hitl_sub.add_parser("resume", help="Check if a gate is resolved (workflow calls this).")
    hitl_resume.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_resume.add_argument("--id", required=True, help="Gate instance ID.")
    hitl_resume.add_argument(
        "--pr-state",
        choices=sorted(PR_STATES),
        help="Actual PR state (OPEN, MERGED, CLOSED). When provided, reconciles gate with reality.",
    )

    hitl_list = hitl_sub.add_parser("list", help="List all gates and their states.")
    hitl_list.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_list.add_argument("--state", choices=("pending", "approved", "rejected"), help="Filter by state.")

    hitl_merge_check = hitl_sub.add_parser("merge-check", help="Check if a merge is allowed by HITL.")
    hitl_merge_check.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_merge_check.add_argument(
        "--type",
        required=True,
        choices=("story_to_feature", "feature_to_develop", "develop_to_main"),
    )
    hitl_merge_check.add_argument("--object", required=True, help="Affected object (branch/feature).")
    hitl_merge_check.add_argument(
        "--pr-state",
        choices=sorted(PR_STATES),
        help="Actual PR state to reconcile before allowing merge.",
    )

    hitl_validate = hitl_sub.add_parser("validate", help="Validate Dedicated Harness HITL config.")
    hitl_validate.add_argument("path", type=Path, help="Dedicated Harness root.")

    hitl_reconcile = hitl_sub.add_parser(
        "reconcile",
        help="Reconcile a gate's state with the actual PR state from GitHub. "
        "Checks for divergences between gate state, PR state, and merge_origin.",
    )
    hitl_reconcile.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_reconcile.add_argument("--id", required=True, help="Gate instance ID.")
    hitl_reconcile.add_argument(
        "--pr-state",
        required=True,
        choices=sorted(PR_STATES),
        help="Actual PR state from GitHub (e.g., OPEN, MERGED, CLOSED).",
    )
    hitl_reconcile.add_argument("--pr-number", type=int, help="PR number for evidence.")

    hitl_record_manual = hitl_sub.add_parser(
        "record-manual-merge",
        help="Record that a human performed the merge directly on GitHub. "
        "Updates the gate with merge_origin=human_manual without executing a merge.",
    )
    hitl_record_manual.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    hitl_record_manual.add_argument("--id", required=True, help="Gate instance ID.")
    hitl_record_manual.add_argument("--by", required=True, help="Human who performed the merge.")
    hitl_record_manual.add_argument("--pr-number", type=int, help="PR number for evidence.")
    hitl_record_manual.add_argument("--note", help="Optional observation.")

    # --- merge (controlled, HITL-gated) ---
    merge_parser = sub.add_parser(
        "merge",
        help="Merge a pull request through the HITL-gated controlled merge path. "
        "This is the ONLY authorized way to merge. Direct merge tools are forbidden.",
    )
    merge_parser.add_argument("--path", type=Path, default=Path("."), help="Project root.")
    merge_parser.add_argument(
        "--type", required=True,
        choices=list(MERGE_TYPE_MAP.keys()),
        help="Type of merge (story_to_feature, feature_to_develop, develop_to_main).",
    )
    merge_parser.add_argument("--object", required=True, help="Affected object/branch name.")
    merge_parser.add_argument("--pr", type=int, required=True, help="Pull request number to merge.")
    merge_parser.add_argument("--owner", help="Explicit expected GitHub owner (optional).")
    merge_parser.add_argument("--repo", help="Explicit expected GitHub repository name (optional).")

    # --- vault ---
    vault_parser = sub.add_parser(
        "vault",
        help="Harness Vault: query knowledge graph, validate, materialize.",
    )
    vault_sub = vault_parser.add_subparsers(dest="vault_command", required=True)

    vault_query = vault_sub.add_parser(
        "query", help="Query the vault knowledge graph."
    )
    vault_query.add_argument("--path", type=Path, default=Path("."), help="Vault root.")
    vault_query.add_argument("--find", help="Search notes by term (title, alias, tag, body).")
    vault_query.add_argument("--follow", help="Expand wikilinks from a note ID.")
    vault_query.add_argument("--graph", action="store_true", help="Show full graph summary.")

    vault_validate = vault_sub.add_parser(
        "validate", help="Validate vault structure, frontmatter, and wikilinks."
    )
    vault_validate.add_argument("--path", type=Path, default=Path("."), help="Vault root.")

    vault_materialize = vault_sub.add_parser(
        "materialize",
        help="Materialize vault notes into a Dedicated Harness (.harness/vault/).",
    )
    vault_materialize.add_argument("--base", type=Path, required=True, help="Base Harness root.")
    vault_materialize.add_argument("--output", type=Path, required=True, help="Dedicated Harness root.")
    vault_materialize.add_argument("--ids", nargs="*", help="Specific note IDs to include (default: all).")
    vault_materialize.add_argument("--base-version", default="unknown", help="Base Harness version.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        from . import __version__

        print(__version__)
        return 0

    if args.command == "validate":
        result = validate_base(args.path) if args.kind == "base" else validate_dedicated(args.path)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "generate":
        result = generate_harness(
            profile_path=args.profile,
            base_version=args.base_version,
            output_path=args.output,
        )
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "preflight":
        result = preflight_github(
            args.path,
            expected_owner=args.owner,
            expected_repo=args.repo,
            record=args.record,
        )
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.ok else 1

    if args.command == "gitignore":
        if args.check:
            result = validate_gitignore(args.path / ".gitignore", args.language)
        else:
            result = generate_gitignore(args.path, args.language)
        print(json.dumps(result, indent=2))
        return 0 if result["valid"] else 1

    if args.command == "branch-check":
        result = check_branch(args.path, expected_branch=args.branch)
        print(json.dumps(result.to_dict(), indent=2))
        return 0 if result.ok else 1

    if args.command == "hitl":
        if args.hitl_command == "gate":
            result = create_gate(
                args.path,
                gate_id=args.gate_id,
                workflow=args.workflow,
                affected_object=args.object,
                reason=args.reason,
                evidence=args.evidence,
                expected_authority=args.authority,
            )
        elif args.hitl_command == "approve":
            result = approve_gate(args.path, args.id, args.by, args.note, args.merge_origin)
        elif args.hitl_command == "reject":
            result = reject_gate(args.path, args.id, args.by, args.note)
        elif args.hitl_command == "resume":
            result = resume_check(args.path, args.id, args.pr_state)
        elif args.hitl_command == "list":
            result = list_gates(args.path, args.state)
        elif args.hitl_command == "merge-check":
            result = check_merge_allowed(args.path, args.type, args.object, args.pr_state)
        elif args.hitl_command == "validate":
            result = validate_dedicated_hitl(args.path)
        elif args.hitl_command == "reconcile":
            result = reconcile_gate(args.path, args.id, args.pr_state, args.pr_number)
        elif args.hitl_command == "record-manual-merge":
            result = record_manual_merge(args.path, args.id, args.by, args.pr_number, args.note)
        else:
            parser.error("unreachable hitl command")
            return 2
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok", False) else 1

    if args.command == "merge":
        result = controlled_merge(
            args.path,
            merge_type=args.type,
            affected_object=args.object,
            pr_number=args.pr,
            owner=args.owner,
            repo=args.repo,
        )
        print(json.dumps(result, indent=2))
        return 0 if result.get("ok") else 1

    if args.command == "vault":
        if args.vault_command == "query":
            vault_root = args.path / "vault" if (args.path / "vault").exists() else args.path
            notes = load_vault(vault_root)
            if not notes:
                print(json.dumps({"ok": False, "error": "No vault notes found"}, indent=2))
                return 1
            if args.graph:
                result = graph_summary(notes)
            else:
                result = query_notes(notes, find=args.find, follow=args.follow)
            print(json.dumps(result, indent=2, default=str))
            return 0 if result.get("ok") else 1
        elif args.vault_command == "validate":
            vault_root = args.path / "vault" if (args.path / "vault").exists() else args.path
            notes = load_vault(vault_root)
            result = validate_vault(notes, vault_root)
            print(json.dumps(result, indent=2, default=str))
            return 0 if result["valid"] else 1
        elif args.vault_command == "materialize":
            result = materialize_vault(
                base_root=args.base,
                dedicated_root=args.output,
                selected_ids=args.ids,
                base_version=args.base_version,
            )
            print(json.dumps(result, indent=2, default=str))
            return 0 if result.get("ok") else 1

    parser.error("unreachable")
    return 2


if __name__ == "__main__":
    sys.exit(main())
