# Evidence Index

## Purpose

Trace important Project Profile claims back to concrete project evidence.

## Evidence types

- specification
- source code
- tests
- configuration
- fixture/data
- repository structure

## Confidence

### High

Directly stated or demonstrated.

### Medium

Strongly inferred from multiple sources.

### Low

Plausible inference requiring confirmation.

## Rule

Low-confidence assumptions must not become silent requirements.

## Legacy independence

Legacy system implementation details (language, framework, database, deployment
infrastructure) are **evidence of the old system's architecture**, not automatic
technology requirements for the successor.

The successor's technology stack is decided by the project's own requirements,
architecture deliberation, and explicit engineering decisions — not by what the
legacy system used.

Exception: when a concrete integration, migration, or compatibility constraint
forces technology alignment, this must be recorded as an explicit requirement
with the constraint's source and scope.
