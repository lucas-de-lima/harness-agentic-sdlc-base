# GitHub Project Model

## Purpose

Define how GitHub Issues and Projects act as the operational system of record for project execution.

GitHub Projects supports table, board, and roadmap views, custom fields, issue types, parent/sub-issue relationships, and linked pull requests. The Agentic SDLC uses these capabilities instead of building a parallel local task-management system.

## Project structure

Each product repository should have one primary GitHub Project.

Recommended views:

1. Board — active execution
2. Table — complete backlog
3. Roadmap — macro planning

The three views are projections of the same underlying work items, not separate backlogs.

## Recommended fields

Keep the field set small.

### Status

- Backlog
- Ready
- In Progress
- In Review
- Blocked
- Done

### Priority

- P0
- P1
- P2
- P3

### Effort

- XS
- S
- M
- L
- XL

### Phase

- Discovery
- Architecture
- Planning
- Implementation
- Verification
- Release

### Risk

- Low
- Medium
- High

Do not add fields unless they support a real decision, filter, workflow, or report.

## Ownership

GitHub Issues and Project fields own work state.

ADRs, README files, design documents, and source code own durable engineering knowledge.

## Project template

The Harness Base should eventually provide a GitHub Project template containing the default views, fields, and workflows. Project-specific harnesses may extend it when justified.
