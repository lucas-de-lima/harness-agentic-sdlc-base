# Branching Policy

## Purpose

Define the mandatory branching model for all product repositories governed by a Dedicated
Harness. This policy is reusable across all projects; no project-specific branching rule
is needed unless it extends this model with a documented justification.

## Mandatory model

```text
main
└── only code approved for release/deploy

develop
└── integration of the next version

feature/<feature>
└── branch of a Feature, created from develop

story/<user-story>
└── branch of a User Story, created from the Feature branch
```

## Branch roles

### main

- Contains only code approved for release or deploy.
- No direct commits; changes arrive only via merge from `develop` after verification
  (WF-006 Code Review approval).
- Tags mark release points.
- Protected: no force-push, no direct push by agents.

### develop

- Integration branch for the next version.
- Receives completed feature branches via merge.
- Periodically or per-release merged into `main`.
- No direct experimental commits; all changes come from feature or story branches.

### feature/<feature-name>

- One branch per Feature (GitHub Issue labeled `feature`).
- Created from `develop`.
- Integrates the Feature's User Stories.
- Merged back to `develop` when the Feature is complete and reviewed.
- Naming: `feature/<kebab-case-feature-name>` (e.g., `feature/authentication-session`).

### story/<user-story-name>

- One branch per User Story (GitHub Issue labeled `user-story`).
- Created from the parent `feature/<feature-name>` branch.
- Contains the implementation of that Story's Tasks.
- Merged back to the parent feature branch when the Story's Tasks are reviewed.
- Naming: `story/<kebab-case-story-name>` (e.g., `story/register-new-user`).

## Creation and merge rules

| Branch | Created from | Merges to |
|---|---|---|
| `develop` | `main` (initial) | `main` (per release) |
| `feature/<name>` | `develop` | `develop` |
| `story/<name>` | `feature/<parent>` | `feature/<parent>` |

- A `story/` branch is never created from `develop` or `main` directly.
- A `feature/` branch is never created from `main` or another `feature/` directly.
- `main` never receives feature or story branches directly.
- Hotfix branches (exception, see below) are created from `main` and merge to both `main`
  and `develop`.

## Hotfix exception

```text
hotfix/<description>
└── created from main
└── merges to main AND develop
```

- Used only for critical production fixes.
- Must be rare and documented.
- Merges to both `main` (for immediate release) and `develop` (to keep integration
  current).

## Agent rules

1. **Never commit to `main` directly.** `main` receives only reviewed merges.
2. **Never commit to `develop` directly.** `develop` receives only feature merges.
3. **Create story branches from the parent feature branch, not from `develop`.**
4. **Create feature branches from `develop`, not from `main`.**
5. **Validate the branch model before starting work.** Use `harnessctl branch-check`
   to confirm the current branch is valid and correctly based.
6. **Do not force-push to `main` or `develop`.**
7. **Do not create branches outside the model** (`experiment/`, `wip/`, personal branches).
   Use the feature/story model; experiments belong in a spike that follows the same flow.

## Relationship to workflows

The branching model is the physical realization of the Feature Execution Model
(see `FEATURE_EXECUTION_MODEL.md`):

| Workflow | Branch context |
|---|---|
| WF-004 Implementation Planning | No branch needed (planning only) |
| WF-005 Implementation | Creates `feature/<name>` from `develop`; then `story/<name>` from `feature/<name>` per Story |
| WF-006 Code Review | Reviews `story/<name>` diff against `feature/<name>`; then `feature/<name>` diff against `develop` |
| WF-007 Release Preparation | Merges `develop` → `main`; tags `main` |

The `feature/` branch is the execution boundary. The `story/` branch is the development
and review boundary. See `FEATURE_EXECUTION_MODEL.md` for the full execution flow.

## Enforcement

The `harnessctl branch-check` command validates:
- The current branch name matches the allowed patterns.
- The branch is based on the correct parent (feature from develop; story from feature).
- `main` and `develop` exist.
- No uncommitted work on `main` or `develop` (agents should not commit there).

If validation fails, the agent must not proceed with implementation.

## Scope

This policy applies to all product repositories governed by a Dedicated Harness. It does
not apply to the Base Harness repository itself, which is developed as a normal software
project (see `BASE_REPOSITORY_OPERATING_MODEL.md`).

## Dedication (no project-specific overrides)

A Dedicated Harness may tighten this policy (e.g., require signed commits, enforce
branch protection rules via GitHub) but must not weaken the branch hierarchy. The
feature → story structure is mandatory.
