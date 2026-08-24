# Go Engineering Standards

**Status:** v0.1
**Scope:** All Go systems produced by Dedicated Harnesses

## 1. Purpose

These standards define the baseline expectation for Go implementation quality without prescribing one universal architecture or coding style.

The objective is **good, idiomatic, maintainable Go appropriate to the system**.

## 2. Core Rule

> Do the simple thing well before doing the sophisticated thing.

An implementation is considered healthy when its abstractions, concurrency, dependencies, project structure, and performance techniques have a clear reason to exist.

## 3. Language and Toolchain

- Use a current stable Go version selected deliberately for the project.
- Pin the minimum Go version in `go.mod`.
- Use `gofmt` and standard Go formatting.
- Keep `go vet` clean unless an exception is documented.
- Use a linter appropriate to the project; avoid enabling rules that create noise without value.
- Prefer standard library functionality when it is sufficient.

## 4. Package Design

- Packages should represent meaningful responsibilities.
- Avoid packages created only to satisfy an arbitrary directory template.
- Keep package APIs small.
- Avoid import cycles.
- Keep dependency direction understandable.
- Prefer concrete types until an abstraction is justified.

## 5. Interfaces

- Define interfaces for behavior, usually close to the consumer.
- Keep interfaces small.
- Do not create interfaces for every struct automatically.
- Avoid interfaces whose only purpose is mocking a concrete implementation without a meaningful boundary.

## 6. Construction and Dependency Management

Prefer explicit construction and constructor injection.

Avoid by default:

- global mutable dependencies;
- service locators;
- reflection-heavy dependency injection frameworks;
- hidden initialization.

Use dependency injection to make ownership and substitution clear, not as a ritual.

## 7. Error Handling

- Treat errors as part of normal program behavior where appropriate.
- Add context when it materially improves diagnosis.
- Preserve useful error identity when callers need to inspect it.
- Do not discard errors silently.
- Avoid panic for ordinary runtime failures.
- Define domain-specific errors only when callers benefit from distinguishing them.

## 8. Context

Use `context.Context` for:

- cancellation;
- deadlines;
- request-scoped metadata when appropriate.

Do not use context as a general-purpose bag for arbitrary application state.

## 9. Concurrency

Concurrency must solve a real problem such as:

- independent work;
- latency hiding;
- bounded background processing;
- throughput requirements;
- naturally asynchronous workflows.

Use the simplest synchronization model that works.

Prefer avoiding shared mutable state when practical.

Always consider:

- cancellation;
- shutdown;
- bounded concurrency;
- ownership of channels;
- goroutine lifetime;
- race conditions.

## 10. HTTP and APIs

For HTTP services:

- keep transport concerns separate from business behavior when the project benefits from that boundary;
- validate external input at the boundary;
- return deliberate status codes;
- keep error responses consistent;
- define request/response contracts clearly;
- support graceful shutdown when the service is long-running.

Use a third-party router only when its value exceeds the cost of the dependency and standard-library routing is insufficient for the project.

## 11. Persistence

- Keep SQL and data access understandable.
- Use transactions only where invariants require atomicity.
- Avoid repositories that merely mirror database CRUD without a useful boundary.
- Keep migrations versioned and reproducible.
- Make connection lifecycle and configuration explicit.

## 12. Testing

The test strategy should match the system.

Use, as appropriate:

- unit tests for meaningful isolated behavior;
- table-driven tests where they improve clarity;
- HTTP handler tests;
- integration tests for real infrastructure boundaries;
- end-to-end tests sparingly;
- benchmarks when performance is actually relevant;
- race detection for concurrency-sensitive code.

Do not optimize for a vanity coverage percentage.

## 13. Observability

Long-running services should have enough logging and health information to understand normal operation and common failure modes.

Add metrics/tracing when they provide real operational value.

Do not build an elaborate observability stack for a tiny standalone API without a reason.

## 14. Configuration

Configuration should be:

- explicit;
- validated at startup where possible;
- environment-friendly for containerized execution;
- free of secrets committed to source control.

## 15. Dependencies

Every dependency introduces:

- maintenance;
- security exposure;
- upgrade cost;
- cognitive load.

Prefer the standard library when it is sufficient.

Add a dependency when it materially improves correctness, capability, maintainability, performance, or integration with an external constraint.

## 16. Performance

Do not optimize speculative bottlenecks.

Prefer:

1. correct design;
2. measurement;
3. targeted optimization;
4. regression protection where performance matters.

## 17. Project Layout

There is no mandatory universal Go layout.

Use the smallest structure that keeps the code understandable.

`cmd/` and `internal/` are useful conventions, not requirements for every repository.

## 18. Security Baseline

At minimum consider:

- input validation;
- authentication/authorization where required;
- secret handling;
- dependency vulnerabilities;
- SQL injection and unsafe query construction;
- insecure network configuration;
- unsafe file/system operations;
- error leakage;
- resource exhaustion.

## 19. Code Review Heuristics

Reviewers should ask:

- Is this simpler than it needs to be, or more complex than it needs to be?
- Are abstractions serving a real boundary?
- Are interfaces necessary?
- Is concurrency justified and safely bounded?
- Are errors actionable?
- Are dependencies justified?
- Does package structure reflect real responsibilities?
- Are tests validating behavior rather than implementation trivia?
- Could a future engineer understand this without oral history?

## 20. Exceptions

A project may deliberately deviate from these standards when there is a documented project-specific reason.

An exception should explain:

- the standard being deviated from;
- the project-specific reason;
- the consequence;
- the review/acceptance decision.
