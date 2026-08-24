# Security Release Model

## Minimum checks

- dependency vulnerability review where tooling exists
- secrets scan or equivalent
- unsafe configuration review
- exposed ports reviewed
- authentication/authorization behavior reviewed when applicable
- error/log output reviewed for credential leakage

## Scope

This is baseline application security verification, not a penetration test.

## Escalation

High-severity security findings block release until explicitly resolved or formally waived.
