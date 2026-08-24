# Harness Generation Rules

## Principle

Generate the smallest Dedicated Harness that can safely and effectively develop the project.

## Required generation order

1. Project Profile
2. Naming
3. Architecture Decision
4. Skill selection
5. Agent selection
6. Tool selection
7. Workflow selection
8. Quality-gate selection
9. Harness validation

## Selection rules

### Skills

Select the minimum useful skill set.

### Agents

Do not instantiate an agent solely because the Base Harness defines it.

A project may omit roles that provide no meaningful value.

### Tools

Use the least-privileged tool set that supports the selected workflow.

### Workflows

Only generate workflows the project needs.

### Policies

Project policies may tighten Base requirements but must not silently weaken them.

## No speculative infrastructure

The Factory must not generate:

- unused services
- unnecessary databases
- message brokers without a use case
- custom MCPs without an approved capability gap
- agent roles without a responsibility
- documentation files that duplicate GitHub work items
