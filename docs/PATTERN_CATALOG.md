# Pattern Catalog

**Status:** v0.1
**Scope:** Harness Base and Dedicated Harnesses

## 1. Purpose

This catalog defines reusable design patterns that agents may consider after the architecture and problem are understood.

Patterns are optional. They are not proof of engineering quality and must never be introduced solely to make a design look sophisticated.

## 2. Pattern Classes

### P1 — Composition and Constructor Injection

Prefer explicit construction and dependency passing over global state, hidden service locators, or reflection-heavy dependency injection.

**Use when:** dependencies need substitution, isolation, or clear ownership.

**Avoid when:** a dependency is stable, local, and direct construction remains clearer.

### P2 — Small Interface / Consumer-Owned Interface

Define interfaces where the consuming behavior needs an abstraction rather than creating interfaces for every concrete type.

**Use when:** substitution, isolation, or multiple implementations provide real value.

**Avoid when:** an interface merely wraps one implementation without a current reason.

### P3 — Adapter

Translate an external API, protocol, or infrastructure representation into the application's expected form.

**Use when:** an external boundary is meaningful or unstable.

### P4 — Repository Boundary

Encapsulate persistence operations behind a domain/application-oriented boundary.

**Use when:** persistence complexity, testing needs, or domain independence justify it.

**Avoid when:** a repository only forwards every CRUD method one-for-one and adds no useful boundary.

### P5 — Service / Use-Case Boundary

Group application behavior around meaningful operations rather than transport handlers.

**Use when:** business operations are reused, coordinated, or contain meaningful rules.

**Avoid when:** a service exists solely to move calls between handlers and repositories.

### P6 — Strategy

Select among interchangeable behaviors through a stable abstraction.

**Use when:** behavior genuinely varies by policy, configuration, or runtime choice.

### P7 — Factory

Centralize creation when object construction has meaningful policy or multiple variants.

**Avoid when:** the factory only calls a constructor.

### P8 — Decorator / Middleware

Wrap behavior to add cross-cutting concerns such as logging, metrics, authentication, tracing, retries, or rate limiting.

**Use when:** the cross-cutting behavior applies consistently across a boundary.

### P9 — Worker Pool

Bound concurrent work using a controlled number of workers.

**Use when:** there is a queue of independent work and concurrency must be bounded.

### P10 — Pipeline

Represent multi-stage processing as explicit sequential/concurrent stages.

**Use when:** the domain or operational problem naturally consists of processing stages.

### P11 — Retry with Backoff

Retry transient failures with bounded attempts and backoff.

**Use when:** failure is demonstrably transient and retrying is safe.

**Never assume:** every error is retryable or every operation is idempotent.

### P12 — Transaction Boundary

Group multiple persistence changes into one atomic operation when the business invariant requires it.

### P13 — Transactional Outbox

Persist an outgoing event/message in the same transaction as the state change, then publish it asynchronously.

**Use when:** reliable event publication is a real requirement.

**Do not use:** merely to demonstrate event-driven design.

### P14 — Cache

Cache expensive or frequently reused data when measurement or a clear performance requirement justifies it.

**Primary concerns:** invalidation, staleness, memory, failure behavior.

### P15 — Idempotency

Design an operation so repeated requests do not create unintended duplicate effects.

**Use when:** retries, duplicate delivery, or repeated client requests are realistic.

### P16 — Circuit Breaker / Bulkhead

Isolate failing or overloaded external dependencies.

**Use only when:** dependency failure behavior and operational resilience make the complexity worthwhile.

## 3. Selection Rule

A pattern should be selected only when all are true:

1. The underlying problem exists.
2. The pattern addresses that problem directly.
3. The complexity introduced is acceptable for the project.
4. The team/agent can explain the trade-off.

## 4. Pattern Non-Goals

This catalog does not require every project to use a pattern.

A project with no explicit need for a pattern may legitimately use direct code.

## 5. Pattern Decision Record

When a non-obvious pattern is introduced, record:

- problem;
- chosen pattern;
- simpler alternative considered;
- benefit obtained;
- new complexity introduced;
- reason the trade-off is acceptable.
