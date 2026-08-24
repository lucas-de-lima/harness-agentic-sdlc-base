# Orchestrator — GitHub Discovery

## Preconditions

1. GitHub MCP is available.
2. The repository is the correct product repository.
3. `DISCOVERY-001` exists.
4. `DISCOVERY-001` is in `Ready`.
5. Project capability policy allows `issues: read` and `projects: read`.
6. The `project-discovery` skill is available.
7. The inherited project specification is present.
8. No conflicting active discovery execution exists.

## Execution

### Step 1 — Read work item

Read:

- Issue title
- Issue body
- Issue type
- Project fields
- parent/sub-issue state
- relevant comments

### Step 2 — Resolve repository

Identify the exact repository associated with the work item.

### Step 3 — Load project context

Load:

- project specification
- applicable `AGENTS.md`
- Dedicated Harness context, if present
- discovery skill

### Step 4 — Execute Discovery

Invoke the Discovery Agent.

### Step 5 — Validate

Validate:

- required Project Profile sections
- naming
- evidence
- absence of production mutations

### Step 6 — Handoff

Produce the Handoff Packet.

### Step 7 — Write bounded evidence

Add one concise execution comment to the Issue.

### Step 8 — Transition

Move:

`Ready → In Review`

only when validation succeeds.

## Block conditions

Stop instead of guessing when:

- repository identity is ambiguous
- the Issue has conflicting project states
- legacy specification is missing
- profile evidence is materially contradictory
- architecture would need to be decided during discovery
