# Architecture Decision Framework

**Status:** v0.1
**Scope:** Architect Agent and Dedicated Harnesses

## 1. Purpose

This framework defines how the Architect Agent reasons about architecture without turning architectural choice into a mechanical score-only exercise.

## 2. Decision Sequence

```text
Understand system
      ↓
Extract architectural requirements
      ↓
Identify constraints
      ↓
Generate plausible candidates
      ↓
Eliminate candidates that do not fit
      ↓
Compare remaining candidates
      ↓
Prefer the simplest sufficient candidate
      ↓
Document trade-offs
      ↓
Produce Architecture Decision + ADR
```

## 3. Hard Constraints vs Preferences

### Hard constraints

A candidate that violates a hard constraint is rejected.

Examples:

- deployment target requires one process;
- regulatory constraint requires a specific persistence model;
- external protocol requires asynchronous consumption;
- latency requirement rules out a particular synchronous design.

### Preferences

Preferences influence the decision but do not automatically eliminate candidates.

Examples:

- easier testing;
- lower operational burden;
- simpler onboarding;
- standard library preference;
- reduced dependency count.

## 4. Comparative Matrix

When multiple candidates survive elimination, compare them qualitatively using:

- fit to requirements;
- complexity introduced;
- maintainability;
- testability;
- operability;
- performance characteristics;
- failure behavior;
- future changeability.

A numerical score may be used as a supporting device, but it must never override explicit architectural reasoning.

## 5. Simplicity Check

Before finalizing any architecture, the Architect Agent must answer:

> What is the simplest architecture that would work?

Then:

> What concrete requirement or risk makes the chosen architecture better than that simpler option?

If the second answer is weak, the architecture should be simplified.

## 6. Architecture Smell Check

The Architect Agent should explicitly inspect for:

- unnecessary layers;
- interfaces with one implementation and no meaningful boundary;
- repositories added only by convention;
- service layers that only forward calls;
- event infrastructure without asynchronous requirements;
- distributed services without independent deployment needs;
- message brokers used as generic plumbing;
- premature abstractions for hypothetical future changes.

## 7. Decision Confidence

The Architecture Decision should classify confidence as:

- **High:** requirements and constraints are well understood;
- **Medium:** some meaningful uncertainty remains;
- **Low:** architecture depends on unresolved product/domain information.

Low-confidence decisions should prefer reversible choices and may trigger a Spike work item.

## 8. Revisit Triggers

Architecture should be reconsidered when:

- a new requirement invalidates a key assumption;
- a major integration is added;
- data ownership changes materially;
- concurrency requirements change materially;
- deployment constraints change;
- repeated implementation friction exposes a boundary problem;
- operational evidence contradicts an architectural assumption.

## 9. Output Contract

The Architect Agent must never output only a label such as:

> "Use Hexagonal Architecture."

It must output a defensible decision containing:

```text
Context
Constraints
Candidates
Decision
Why
Why not the simpler option
Trade-offs
Risks
Revisit triggers
```

