# GitHub Project Bootstrap

## Purpose

Define the Project configuration that the Harness Base expects from each product.

## Recommended Project

One primary Project per product repository.

## Views

- Board
- Table
- Roadmap

Projects currently supports these layouts. citeturn501381search0

## Fields

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

## Hierarchy

Use GitHub issue parent/sub-issue relationships for:

Epic
└── Feature
    └── User Story
        └── Task

GitHub supports multiple levels of sub-issues and exposes their progress to Projects. citeturn501381search4

## Issue types

Prefer GitHub Issue Types where available.

The REST and GraphQL APIs expose organization/repository issue types and Project issue-type fields. citeturn501381search3turn501381search6turn501381search0
