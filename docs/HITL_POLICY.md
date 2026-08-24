# Human-in-the-Loop (HITL) Policy

## Purpose

Define the mandatory human-gate capability for all product repositories governed by a
Dedicated Harness. Agents can execute technical work, but decisions of human authority
cannot be executed automatically.

HITL is implemented as policy + workflow gates + auditability, not as a README
instruction.

## Principle

> When a Human Gate is pending, the workflow must PAUSE.

No gate may be substituted by polling, timeout, automatic approval, or interpretation of
silence.

## Mandatory Human Gates

These gates require explicit human approval. They cannot be automated, bypassed, or
inferred:

| Gate ID | Trigger | Authority |
|---|---|---|
| `HG-PRODUCT` | Product decision (scope, contract, requirements) | Product owner |
| `HG-ARCHITECTURE` | Material architecture change (requires ADR) | Architect / human |
| `HG-SCOPE` | Material scope change beyond the approved Feature | Product owner |
| `HG-MERGE-STORY` | Merge `story/<name>` → `feature/<name>` | Human (reviewer or owner) |
| `HG-MERGE-FEATURE` | Merge `feature/<name>` → `develop` | Human |
| `HG-MERGE-DEVELOP` | Merge `develop` → `main` | Human (release authority) |
| `HG-RELEASE` | Release approval / tag / publish | Human (release authority) |
| `HG-SECURITY-EXCEPTION` | Security policy exception | Security authority / human |
| `HG-DESTRUCTIVE` | Destructive or irreversible action (data loss, force-push, delete) | Human |
| `HG-DEPLOY` | Production deployment (when applicable) | Human (deploy authority) |

## Agent autonomy

### Agents MAY

- create branches (`feature/`, `story/`, `hotfix/`)
- implement Tasks and Stories
- execute tests, linters, formatters
- create pull requests (PR creation is automatable)
- review code (independent review)
- fix approved review findings
- prepare PRs for integration
- produce execution evidence

### Agents MAY NOT

- merge (any merge: story→feature, feature→develop, develop→main)
- close a Human Gate
- approve their own change
- promote code to `develop` or `main` without human approval
- transform a blocked decision into an approved one by inference
- auto-approve via timeout, silence, or polling
- call `github_merge_pull_request` or any equivalent merge API directly — the only
  authorized merge path is `harnessctl merge`

## Authorized merge path

The `harnessctl merge` command is the **only** authorized mechanism for executing a
harness-controlled merge. It enforces the following checks before allowing the merge to
proceed:

1. **GitHub identity preflight** — validates the repository's GitHub identity
2. **HITL gate check** — reads `.harness/hitl/gates.json` and confirms the required
   `HG-MERGE-*` gate is in `approved` state
3. **PR state reconciliation** — checks the actual PR state on GitHub before proceeding;
   if PR is already `MERGED`, no merge is executed (see Manual Merge Recognition below)
4. **Merge block** — if the gate is missing, `pending`, or `rejected`, the merge is BLOCKED
5. **Evidence recording** — on successful merge, adds merge evidence to the gate record
   with `merge_origin: "harness_controlled"`

## Manual merge recognition

A Human Gate represents:

> "This decision belongs to the human."

It does NOT automatically mean "the agent will merge after the human clicks Approve."

The following merge paths are both valid:

| Path | merge_origin | Description |
|---|---|---|
| Human reviews PR on GitHub and clicks Merge | `human_manual` | Human executes merge directly. Gate is recorded as approved with `merge_origin: human_manual`. No automated merge is executed. |
| Human approves the gate via `harnessctl hitl approve` | `harness_controlled` | Human delegates the merge execution to `harnessctl merge`. Gate is approved; automated merge is allowed. |

### Resume behavior with PR state

Before any resume or merge, the workflow MUST consult the actual PR state on GitHub:

| PR state | Gate state | Workflow action |
|---|---|---|
| `MERGED` | `pending` or `approved` | Gate considered satisfied. Continue workflow. Record `merge_origin: human_manual` if not already set. Do NOT execute merge again. |
| `OPEN` | `pending` | Stay PAUSED. Await human decision. |
| `OPEN` | `approved` | Continue — `harnessctl merge` may execute the merge (harness_controlled). |
| `CLOSED` (no merge) | `approved` or `pending` | Return to correction state. PR was closed without merging. |

### Merge origin tracking

Every merge that occurs through the HITL system records a `merge_origin`:

- `harness_controlled` — merge was executed by `harnessctl merge` after gate approval
- `human_manual` — merge was executed directly by a human on GitHub (detected during
  resume/reconciliation)

The `reconcile` command detects if a PR is `MERGED` but the gate still has no
`merge_origin`, and surfaces it as an issue for manual resolution via
`harnessctl hitl record-manual-merge`.

### Usage

```bash
# Story → Feature merge
harnessctl merge --path . --type story_to_feature --object story/register-user --pr 41

# Feature → develop merge
harnessctl merge --path . --type feature_to_develop --object feature/auth --pr 43

# develop → main merge
harnessctl merge --path . --type develop_to_main --object develop --pr 50
```

### Merge type to gate mapping

| `--type` | Gate required | Description |
|---|---|---|
| `story_to_feature` | HG-MERGE-STORY | Merge story/\<name\> → feature/\<name\> |
| `feature_to_develop` | HG-MERGE-FEATURE | Merge feature/\<name\> → develop |
| `develop_to_main` | HG-MERGE-DEVELOP | Merge develop → main |

### Enforcement

A merge that bypasses `harnessctl merge` (e.g., calling `github_merge_pull_request` directly,
clicking the GitHub "Merge" button, or using `gh pr merge` outside of `harnessctl`) is a
**policy violation**. It will be flagged by `make validate` (see validation script
`scripts/validate_hitl_merge.py`).

## Human Gate contract

Each gate instance must contain:

| Field | Description |
|---|---|
| `gate_id` | One of the mandatory gate IDs (e.g., `HG-MERGE-STORY`) |
| `instance_id` | Unique identifier for this gate instance (auto-generated) |
| `workflow` | The workflow that created the gate (e.g., `WF-005`, `WF-006`, `WF-007`) |
| `affected_object` | The work item, branch, or artifact affected (e.g., `story/register-user`, `feature/auth`) |
| `reason` | Why this gate is required |
| `evidence` | Supporting evidence (diff summary, test results, review outcome) |
| `state` | `pending` / `approved` / `rejected` |
| `expected_authority` | The role or person expected to approve |
| `created_at` | ISO-8601 timestamp when the gate was created |
| `decided_at` | ISO-8601 timestamp when the human decided (null while pending) |
| `decision` | `approved` / `rejected` (null while pending) |
| `decided_by` | Human identifier who decided (null while pending) |
| `note` | Optional human observation |
| `merge_origin` | `human_manual` / `harness_controlled` / null (set after merge) |
| `merge_evidence` | Array of merge records (set after merge) |

## Pause and resume

When a workflow pauses at a Human Gate:

1. **Preserve execution state** — all completed work, evidence, and branch state remain.
2. **Record the exact pause point** — the gate instance, workflow step, and work item.
3. **Record what is awaiting approval** — the gate contract above.
4. **Allow resumption without repeating completed work** — on approval, the workflow
   continues from the gate; on rejection, the workflow returns to the correct prior state
   (e.g., Story In Progress, Feature In Progress).

### State file

Gate state is persisted in `.harness/hitl/gates.json` inside the product repository. This
file is the audit trail and the resume point. It is NOT a substitute for GitHub state;
it records the human-gate lifecycle.

### Reconcile command

Use `harnessctl hitl reconcile --id <instance-id> --pr-state <OPEN|MERGED|CLOSED>` to
compare the gate's expected state against the actual PR state on GitHub. This detects:

- PR merged but gate still pending (auto-satisfy on resume)
- PR open but gate approved (ready for harness_controlled merge)
- PR closed without merge but gate approved (divergence requiring correction)
- Missing merge_origin on a merged PR
- Missing merge_evidence for a harness_controlled merge

### Record manual merge

After detecting a manual human merge (PR = MERGED, gate = pending), call
`harnessctl hitl record-manual-merge --id <instance-id> --by <who> --pr-number <n>` to
update the gate record with `merge_origin: human_manual` without executing a new merge.

### Resume rules

| Gate state on resume with no PR context | Action |
|---|---|
| `approved` | Continue workflow past the gate |
| `rejected` | Return workflow to the state before the gate (e.g., In Progress) |
| `pending` | Stay paused; do not proceed |
| (gate not found) | Halt: cannot resume without a gate record |

### Resume rules with PR state

| PR state | Gate state | Action |
|---|---|---|
| `MERGED` | any | Consider gate satisfied. Record `merge_origin: human_manual` if missing. Continue workflow. Do not merge again. |
| `OPEN` | `pending` | Stay PAUSED |
| `OPEN` | `approved` | Continue. `harnessctl merge` may execute (harness_controlled). |
| `OPEN` | `rejected` | Return to correction state |
| `CLOSED` | any | Return to correction state. PR closed without merge.

## GitHub integration

- **PR creation** may be automated by the agent.
- **PR merge** may NOT be automated. The agent prepares the PR and requests human approval
  via a `HG-MERGE-*` gate.
- The PR is evidence associated with the gate; the gate is the authority, not the PR
  merge button.

## Feature execution pause points

```text
Story complete (implemented + validated + reviewed)
    ↓
Human Gate: HG-MERGE-STORY (merge story/<name> → feature/<name>)
    ↓ [human approves]
Story Done; continue to next Story
    ↓
Feature complete (all Stories Done + integration reviewed)
    ↓
Human Gate: HG-MERGE-FEATURE (merge feature/<name> → develop)
    ↓ [human approves]
Feature Done
    ↓
Release Candidate ready
    ↓
Human Gate: HG-RELEASE (release / tag / publish)
    ↓
Human Gate: HG-MERGE-DEVELOP (merge develop → main) [if not already on main]
    ↓
Released
```

## Auditability

Every human approval or rejection must be recorded as evidence:

- The gate instance (with all fields) is the audit record.
- The gate file (`.harness/hitl/gates.json`) is the durable audit trail.
- Rejections include the reason and the state the workflow returned to.
- Approvals include the approver identity and timestamp.

This audit trail is separate from GitHub PR history. It records the *decision*, not just
the *merge*.

## Dedicated Harness inheritance

A Dedicated Harness inherits the HITL policy from the Base Harness. It may materialize:

- which gates are applicable to the project (all mandatory gates apply unless the project
  genuinely does not use a workflow — e.g., a project with no release step may mark
  `HG-RELEASE` as not-applicable with justification);
- who the approver is, when configurable (expected_authority);
- which additional project-specific gates are required (a project may add gates but not
  remove mandatory ones).

A Dedicated Harness **cannot remove a mandatory Human Gate** from the Base. Any attempt to
do so is a policy violation.

## Enforcement

The `harnessctl hitl` command family enforces the policy:

- `hitl gate` — create a pending gate (agent calls this when reaching a pause point)
- `hitl approve` — human approves a gate (records decision, allows resume; optionally sets
  `--merge-origin human_manual|harness_controlled`)
- `hitl reject` — human rejects a gate (records decision, returns workflow)
- `hitl resume` — check if a gate is resolved and report whether the workflow may continue
  (accepts optional `--pr-state` to reconcile with actual PR state)
- `hitl reconcile` — compare gate state against actual PR state (OPEN/MERGED/CLOSED) and
  report any divergences
- `hitl record-manual-merge` — record that a human performed the merge directly on GitHub
- `hitl list` — list all gates and their states

Agents call `hitl gate` to pause. Humans call `hitl approve` or `hitl reject`. The
workflow calls `hitl resume` with `--pr-state` to check whether it may proceed.

## Scope

This policy is generic and applies to all Dedicated Harnesses. No project-specific HITL
rule is needed unless it extends this model with additional gates.

## Relationship to existing policies

- `WORKFLOW_GUARDRAILS.md` — HITL is a mandatory guardrail.
- `WORKFLOW_FAILURE_MODEL.md` — "Human decision required" failure class maps to HITL gates.
- `FEATURE_EXECUTION_MODEL.md` — HITL pause points are the merge boundaries.
- `BRANCHING_POLICY.md` — merges require HITL gates; branches do not.
- `IMPLEMENTATION_REVIEW_CONTRACT.md` — review approval is distinct from merge approval;
  review is agent-performed, merge is human-gated.
