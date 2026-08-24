---
name: architecture-review
description: Independently review an architecture decision and ADR against the Project Profile, architecture catalog, review criteria, and evidence. Use after architecture deliberation and before implementation planning. Approve, request changes, or block; do not implement fixes.
---

# Architecture Review

## Purpose

Independently determine whether the architecture decision is ready for downstream implementation planning.

## Inputs

- Project Profile
- Architecture Decision
- ADR
- Architecture Catalog
- Architecture Review Criteria
- previous execution evidence

## Procedure

1. Read the Project Profile.
2. Read the Architecture Decision and ADR.
3. Identify the simplest viable architecture claimed by the decision.
4. Verify that alternatives are plausible and rejection reasons are evidence-based.
5. Evaluate requirements fit.
6. Evaluate complexity fit.
7. Evaluate traceability from evidence to rationale.
8. Evaluate risks and future evolution triggers.
9. Identify findings and severity.
10. Produce Review Report.
11. Select one outcome:
   - Approved
   - Changes Requested
   - Blocked

## Independence rule

Do not assume the Architect Agent's conclusion is correct.

Do not reject merely because you would have chosen a different architecture.

Judge against requirements, evidence, and governing policy.

## Boundaries

Do not modify production code.
Do not rewrite the Architecture Decision.
Do not implement fixes.
Do not change GitHub outside the review workflow contract.

## Approval

Approve only when:

- no Blocking findings exist
- no unresolved Major issue remains that materially affects correctness
- required gates have evidence
- residual risks are acceptable and documented

## Changes Requested

Use when the artifact is fundamentally reviewable but needs specific correction.

## Blocked

Use when required evidence or prerequisites are unavailable or contradictory.
