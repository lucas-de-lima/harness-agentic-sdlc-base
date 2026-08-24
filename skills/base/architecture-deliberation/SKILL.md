---
name: architecture-deliberation
description: Evaluate a project profile against the approved architecture catalog and produce an evidence-backed architecture decision. Use after discovery and before implementation planning. Explicitly compare the simplest viable architecture with more complex candidates and record trade-offs, rejected alternatives, assumptions, and future evolution triggers.
---

# Architecture Deliberation

## Purpose

Select the simplest architecture that satisfies the system requirements with acceptable trade-offs.

## Inputs

- approved Project Profile
- architecture catalog
- architecture decision framework
- project-specific constraints
- known technical context

## Procedure

1. Read the Project Profile completely.
2. Separate explicit requirements from inferred behavior.
3. Identify the simplest viable architecture.
4. Select plausible alternatives from the approved architecture catalog.
5. Compare candidates using:
   - domain fit
   - complexity fit
   - integration fit
   - persistence fit
   - concurrency fit
   - testability
   - operational burden
   - evolvability
6. Identify architecture-driving evidence.
7. Reject alternatives with explicit rationale.
8. Select the architecture.
9. Record assumptions and residual risks.
10. Identify future conditions that would justify architectural evolution.
11. Produce the Architecture Decision and ADR-ready output.

## Anti-overengineering rule

Do not choose a more complex architecture because it is:

- more popular
- more scalable in the abstract
- more impressive
- familiar to the implementer
- theoretically reusable

Complexity must have a concrete system benefit.

## Architecture boundary

Do not implement code.

Do not create dependencies.

Do not decide detailed library choices unless they are necessary to validate the architecture.

## Required output

The output must include:

- selected architecture
- simplest viable baseline
- candidate alternatives
- comparison
- rationale
- rejected alternatives
- consequences
- assumptions
- risks
- future evolution trigger
- unresolved questions
