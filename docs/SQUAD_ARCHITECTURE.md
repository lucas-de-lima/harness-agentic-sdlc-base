# Squad Architecture

## Purpose

The squad is a small set of specialized agents coordinated by an Orchestrator.

The default squad is intentionally small.

## Core Roles

### Orchestrator
Owns workflow progression and delegation. It coordinates; it should not become the default implementation agent.

### Discovery Agent
Builds and updates understanding of requirements, domain, constraints, and legacy behavior.

### Architecture Agent
Evaluates architecture, patterns, major technical decisions, and ADRs.

### Go Engineer
Implements approved work in Go.

### Test Engineer
Designs and implements appropriate automated tests and validates test strategy.

### Reviewer
Performs independent code and design review.

### Security Reviewer
Checks security-relevant behavior, dependencies, configuration, and exposed surfaces.

### Documentation Agent
Maintains durable project documentation.

## Separation of Concerns

The agent that implements a significant change should not be the sole authority approving that change.

The Orchestrator should avoid writing production code except for trivial orchestration/configuration changes.

## Project Specialization

The Dedicated Harness may:

- add project-specific agents
- restrict or expand responsibilities
- add domain-specific skills
- add project-specific review gates

It must not violate the Base Constitution.
