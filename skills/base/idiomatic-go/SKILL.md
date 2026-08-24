---
id: "idiomatic-go"
name: "Idiomatic Go"
version: "0.1.0"
scope: "base"
purpose: "Guide implementation toward clear, idiomatic Go without unnecessary abstraction."
triggers:
  - "Go code is being designed or modified"
inputs:
  - "current code"
  - "project architecture decision"
  - "relevant Go engineering standards"
outputs:
  - "implementation guidance"
  - "review findings"
dependencies:
  - "go-engineering-standards"
validation:
  - "go test ./..."
  - "go vet ./..."
forbidden_behaviors:
  - "introduce abstraction solely to demonstrate a pattern"
  - "add interfaces without a concrete need"
  - "use concurrency without a demonstrated benefit"
---

# Purpose

Guide implementation toward clear, idiomatic Go while preserving the project's chosen level of complexity.

# When to Apply

Use when designing, implementing, or reviewing Go code.

# Inputs

- Current implementation or proposed design.
- Project Architecture Decision.
- Applicable Go Engineering Standards.

# Procedure

1. Prefer the simplest design that satisfies the stated requirements.
2. Use standard library capabilities when they are sufficient.
3. Introduce abstractions only when they improve a concrete boundary.
4. Prefer explicit control flow and error handling.
5. Treat concurrency as a tool for a demonstrated requirement, not as decoration.
6. Check the project's architecture before introducing new layers.

# Expected Outputs

- Implementation recommendations or review findings.
- Explicitly stated trade-offs when a non-obvious technique is proposed.

# Validation

At minimum, run the project's applicable formatting, tests, and static checks.

# Failure / Escalation

Escalate when a proposed implementation conflicts with the approved project architecture or a higher-priority policy.

# Examples

A small HTTP API does not need a repository abstraction merely because a database exists.
