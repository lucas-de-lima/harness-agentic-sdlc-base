# Dedicated Harness Capability Selection

## Principle

The Dedicated Harness receives the smallest useful capability set.

## Selection inputs

- Project Profile
- Architecture Decision
- workflow requirements
- project constraints
- actual integrations

## Candidate capabilities

### Agents

Possible:

- discovery
- architect
- architecture reviewer
- planner
- go engineer
- code reviewer
- release reviewer

A project need not receive all of them.

### Skills

Select only skills required by enabled workflows.

### Tools

Select only required tool capabilities.

### Policies

Project-specific rules may tighten Base policies.

## Example

A very small API may legitimately receive:

```text
agents:
- planner
- go-engineer
- code-reviewer

skills:
- implementation-planning
- go-engineer
- code-review
```

Discovery/architecture artifacts remain available as completed project context even when their active workflows are disabled.
