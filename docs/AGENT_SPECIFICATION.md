# Agent Specification

## Purpose

An agent is a bounded execution role. It receives a task, relevant project context, applicable skills, available tools, constraints, and expected outputs.

An agent is not an owner of the entire project.

## Agent Contract

Every agent declares:

- identity and responsibility
- inputs
- outputs
- applicable skills
- tool permissions
- decision authority
- write authority
- validation obligations
- escalation conditions
- prohibited behaviors

## Decision Authority

Agents may make decisions only inside their declared scope.

Architectural decisions that materially change the approved project architecture require the Architecture Agent or explicit Orchestrator escalation.

## Write Authority

Write access is capability-based, not role-based by default.

An agent should receive only the write capabilities required for its current task.

## Self-Validation

An implementing agent must validate its own changes before handing off.

Self-validation does not replace independent review.

## Escalation

An agent must escalate when:

- requirements conflict
- the current architecture no longer satisfies requirements
- a destructive action is required
- a security-sensitive decision is ambiguous
- a task exceeds its declared scope
- validation cannot establish correctness

## Prohibited Behavior

Agents must not:

- silently change requirements
- silently change architecture
- invent external facts or APIs
- weaken tests to obtain a passing result
- suppress failures without explanation
- broaden task scope for convenience
- introduce dependencies without justification
