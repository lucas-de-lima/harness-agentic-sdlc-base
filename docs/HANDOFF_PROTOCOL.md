# Handoff Protocol

Agents communicate through explicit task handoffs.

## Required Handoff Contents

A handoff must state:

1. task completed or blocked
2. files changed
3. decisions made
4. validation performed
5. known risks or unresolved questions
6. recommended next step

## Handoff States

- `ready` — work is complete and validated
- `needs-review` — work is ready for independent review
- `blocked` — execution cannot continue
- `needs-decision` — a scoped decision is required
- `failed-validation` — expected validation did not pass

## No Hidden State

An agent must not rely on undocumented assumptions from its own previous turn. Relevant state must exist in project artifacts, GitHub work items, or the explicit handoff.

## Rejection

A receiving agent may reject a handoff when required information, validation, or scope boundaries are missing.
