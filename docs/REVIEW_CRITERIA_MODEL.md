# Review Criteria Model

## Review dimensions

Every review selects criteria from the relevant governing catalog.

For Architecture:

1. requirement fit
2. simplicity
3. evidence traceability
4. alternatives
5. trade-off quality
6. scope compliance
7. future evolution
8. risk disclosure

## Severity

### Blocking

A defect that makes the artifact unsafe or invalid to approve.

Examples:

- architecture contradicts explicit requirements
- major requirement invented without evidence
- forbidden complexity without justification
- missing mandatory decision evidence

### Major

Significant issue that should be corrected before approval.

### Minor

Non-blocking improvement.

## Decision rule

A blocking defect cannot coexist with `Approved`.

A Major issue normally yields `Changes Requested`.

Minor findings may be accepted with explicit rationale.
