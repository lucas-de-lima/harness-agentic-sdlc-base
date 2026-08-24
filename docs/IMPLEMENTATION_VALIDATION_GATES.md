# Implementation Validation Gates

## Per-Story gates (before Story In Review)

### Gate 1 — Scope

All changes can be explained by the Story and its Tasks.

### Gate 2 — Behavior

Story acceptance criteria are satisfied.

### Gate 3 — Tests

Relevant tests exist and pass.

### Gate 4 — Go quality

Formatting and standard checks pass.

### Gate 5 — Diff

The Story diff (against `feature/<name>`) contains no accidental or unrelated changes.

### Gate 6 — Architecture

The implementation remains consistent with the approved Architecture Decision.

### Gate 7 — Handoff

Story implementation evidence and unresolved issues are recorded.

A failed gate prevents the Story from entering In Review.

## Per-Feature gates (before Feature In Review)

### Gate F1 — Story completeness

All Stories in the Feature are Done (merged to `feature/<name>`).

### Gate F2 — Integration

The Feature's Stories integrate correctly on `feature/<name>` (no conflicts, combined
behavior works).

### Gate F3 — Feature diff

The Feature diff (against `develop`) contains no accidental or unrelated changes.

### Gate F4 — Architecture

The Feature as a whole remains consistent with the approved Architecture Decision.

### Gate F5 — Handoff

Feature-level execution evidence, integration results, and unresolved issues are recorded.

A failed gate prevents the Feature from entering In Review.
