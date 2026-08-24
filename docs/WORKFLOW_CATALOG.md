# Workflow Catalog

## Base workflows

### WF-001 Project Discovery

Input:
- legacy project specification

Output:
- Project Profile
- candidate name
- identified uncertainties

Terminal:
- profile is complete enough for architecture deliberation

### WF-002 Architecture Deliberation

Input:
- Project Profile

Output:
- Architecture Decision
- ADR(s)
- architecture constraints

Terminal:
- architecture accepted or escalated

### WF-003 Harness Generation

Input:
- Project Profile
- Architecture Decision

Output:
- Dedicated Harness

Terminal:
- harness passes structural validation

### WF-004 Work Item Planning

Input:
- feature/requirement

Output:
- GitHub work-item hierarchy
- acceptance criteria
- dependencies

Terminal:
- work is Ready

### WF-005 Implementation

Input:
- Ready Feature (default) or Ready Task (small work)

Output:
- source changes on `feature/` and `story/` branches
- tests
- execution evidence
- Stories In Review

Terminal:
- Feature is In Review or Blocked

### WF-006 Verification

Input:
- Story In Review (per-Story review)
- Feature In Review (integration review when all Stories Done)

Output:
- test/review evidence
- approved Stories → merged to `feature/`
- approved Feature → merged to `develop`

Terminal:
- approved or returned to In Progress

### WF-007 Release Preparation

Input:
- approved project

Output:
- release-ready repository
- documentation
- operational evidence

Terminal:
- Release-ready or Blocked

## Project-specific workflows

Projects may add workflows only when the domain requires them.

Examples:

- migration
- async job processing
- external integration verification
- benchmark suite
- data import
