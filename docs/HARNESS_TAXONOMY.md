# Harness Taxonomy

**Status:** Draft v0.1
**Scope:** Harness Base and all Dedicated Harnesses

This document defines the conceptual units of the Agentic SDLC and the relationship between them.

## 1. The Core Chain

```text
Requirement
    ↓
Architecture
    ↓
Pattern
    ↓
Skill
    ↓
Agent
    ↓
Tool / MCP
    ↓
Workflow
    ↓
Quality Gate
```

These units are related, but they are not interchangeable.

## 2. Requirement

A statement of behavior, constraint, goal, or quality expectation that the system must satisfy.

Examples:

- user can create an account;
- API must persist data;
- operation must be idempotent;
- deployment must be reproducible;
- response must be returned within a defined target.

Requirements originate from the product/domain and are tracked operationally in GitHub.

## 3. Architecture

The high-level structural approach used to organize the system and its major responsibilities.

Examples:

- Simple application
- Layered architecture
- Modular architecture
- Hexagonal / Ports and Adapters
- Modular Monolith
- Event-driven architecture

Architecture answers:

> How should the major parts of this system be organized and interact?

Architecture is selected per project.

## 4. Pattern

A reusable solution approach for a recurring design problem.

Examples:

- repository abstraction when genuinely useful;
- adapter;
- dependency injection through constructors;
- worker pool;
- pipeline;
- transactional outbox;
- retry with backoff.

Pattern answers:

> How should we solve this recurring structural problem inside the chosen architecture?

Patterns are optional and must be justified by the problem.

## 5. Skill

A bounded body of knowledge and operating procedure that tells an agent how to perform a class of engineering work.

A skill should contain:

- purpose;
- applicability;
- inputs;
- procedure;
- constraints;
- validation criteria;
- common failure modes.

Examples:

- idiomatic-go;
- go-http-api;
- go-testing;
- database-migrations;
- docker-runtime;
- security-review;
- architecture-selection.

A skill is not an autonomous agent.

## 6. Agent

A role with responsibility for making decisions or performing work.

Examples:

- Orchestrator;
- Discovery Agent;
- Architect;
- Engineer;
- Test Engineer;
- Reviewer;
- Security Reviewer;
- Documentation Agent.

An agent uses skills and tools to accomplish its responsibility.

## 7. Tool / MCP

An external capability available to an agent.

Examples:

- filesystem access;
- Git operations;
- GitHub API;
- Docker operations;
- database inspection;
- test execution;
- code search.

A tool provides capability. It does not define the engineering decision to use that capability.

## 8. Workflow

An orchestrated sequence of activities, decisions, and handoffs that moves work from one state to another.

Examples:

- project discovery;
- architecture decision;
- implementation cycle;
- code review;
- release preparation.

A workflow should define:

- entry conditions;
- participating agents;
- required inputs;
- outputs/artifacts;
- validation;
- exit conditions;
- failure/retry behavior.

## 9. Quality Gate

A condition that must be satisfied before work may advance.

Examples:

- build passes;
- unit tests pass;
- architecture decision exists;
- security review has no blocking findings;
- Docker image builds;
- acceptance criteria are satisfied.

A quality gate is evidence-based, not an agent's opinion alone.

## 10. Artifact

A durable output of a workflow.

Examples:

- Project Brief;
- Architecture Decision;
- ADR;
- implementation plan;
- test report;
- review report;
- release notes.

Artifacts are different from GitHub work items.

## 11. Work Item

An operational unit of planned work tracked in GitHub.

Recommended initial types:

- Epic
- Feature
- User Story
- Task
- Bug
- Spike
- Architecture Decision

Work items are the operational state of the project.

## 12. Project Context

The durable body of information that defines the specific system.

A Dedicated Harness may contain:

- domain glossary;
- project brief;
- architecture decision;
- system constraints;
- technology choices;
- conventions;
- known risks;
- project-specific skills;
- agent policies.

## 13. Base Capability vs Project Capability

Every reusable capability should be classified as either:

### Base Capability

Applicable across multiple projects.

### Project Capability

Useful only for one specific project or domain.

Do not promote a project capability to the base without evidence that it generalizes.

## 14. Composition Model

The Dedicated Harness is composed from the base plus project-specific information:

```text
Base Skills
+ Base Agents
+ Base Policies
+ Base Tool Contracts
+ Project Context
+ Project Skills
+ Project Policies
+ Project Architecture
= Dedicated Harness
```

## 15. Decision Ownership

| Unit | Primary question |
|---|---|
| Requirement | What must be true? |
| Architecture | How are major responsibilities organized? |
| Pattern | How do we solve a recurring structural problem? |
| Skill | How should an agent perform a type of work? |
| Agent | Who is responsible for the work/decision? |
| Tool/MCP | What capability can the agent invoke? |
| Workflow | In what sequence does work move? |
| Quality Gate | What evidence allows work to advance? |
| Artifact | What durable knowledge/result was produced? |
| Work Item | What piece of work is currently tracked? |

## 16. Taxonomy Rules

1. Do not create a new category when an existing one is sufficient.
2. Do not turn every instruction into a skill.
3. Do not create an agent when a workflow or skill is enough.
4. Do not create an MCP when an existing tool is sufficient.
5. Do not encode temporary GitHub work state as durable documentation.
6. Keep project-specific knowledge out of the base unless it demonstrably generalizes.
7. Favor a small number of well-defined primitives over a large number of overlapping abstractions.

## 17. Definition of Done for the Taxonomy

This taxonomy is complete for v1 when:

- every planned harness component can be classified unambiguously;
- the team can distinguish architecture from pattern, skill, agent, tool, workflow, and quality gate;
- base capabilities can be separated from project-specific capabilities;
- the taxonomy is sufficient to design the first Dedicated Harness without inventing new categories.
