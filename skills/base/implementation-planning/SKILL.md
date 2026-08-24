---
name: implementation-planning
description: Transform an approved Project Profile and Architecture Decision into a minimal executable GitHub work breakdown of Epics, Features, User Stories, and Tasks with testable acceptance criteria, dependencies, sequencing, risks, and non-goals. Use after architecture approval and before implementation.
---

# Implementation Planning

## Purpose

Turn approved engineering intent into executable work.

## Inputs

- Project Profile
- approved Architecture Decision
- ADR
- Architecture Review Report
- project constraints
- existing GitHub work state

## Procedure

1. Read approved architecture and review evidence.
2. Identify the major system outcome.
3. Define the Epic.
4. Decompose into Features.
5. Decompose Features into independently understandable Stories.
6. Define concrete Tasks.
7. Add testable acceptance criteria.
8. Identify only material dependencies.
9. Identify parallelizable work.
10. Record important non-goals.
11. Assign initial priority, effort, phase, and risk.
12. Validate completeness.
13. Create the GitHub work breakdown.

## Anti-bloat rule

Do not create:

- a Task for every function
- Stories that exist only to organize code
- duplicate documentation tasks
- speculative future features
- infrastructure work without a requirement

## Architecture boundary

Planning must remain consistent with the approved architecture.

If a needed task would materially change architecture, stop and escalate back to Architecture Deliberation.

## Output

Produce:

- Epic
- Feature
- User Story
- Task
- acceptance criteria
- dependencies
- sequencing
- non-goals
- risks
- planning evidence

## Completion

Planning is complete only when the Go Engineer can begin the first Ready task without having to invent missing product scope or architecture.
