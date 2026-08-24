# Validation Script: HITL Merge Enforcement

Scans the Git merge history of a Dedicated Harness repository and verifies that every
merge has a corresponding approved HITL gate recorded in `.harness/hitl/gates.json`.

This script is designed to be called from `make validate` and CI pipelines.

## What it checks

| Check | Description |
|---|---|
| All merges into `develop` have an approved HG-MERGE-FEATURE | Feature merges require human gate |
| All merges into `main` have an approved HG-MERGE-DEVELOP | Release merges require human gate |
| All story→feature merges have an approved HG-MERGE-STORY | Story merges require human gate |
| Merge evidence recorded in gates.json | Each merge leaves an audit trail |

## Exit codes

- 0 — all merges are compliant
- 1 — one or more merges missing required gate approval

## Bypass detection

Detects merges performed directly (e.g., via `github_merge_pull_request` or `gh pr merge`)
without a corresponding `harnessctl merge` call by cross-referencing merge commits against
gate records.