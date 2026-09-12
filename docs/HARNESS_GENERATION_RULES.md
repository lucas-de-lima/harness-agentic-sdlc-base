# Harness Generation Rules

## Principle

Generate the smallest Dedicated Harness that can safely and effectively develop the project.

## Required generation order

1. Project Profile
2. Naming
3. Architecture Decision
4. Skill selection
5. Squad discovery and creation
6. Agent selection
7. Tool selection
8. Workflow selection
9. Quality-gate selection
10. Harness validation

## Selection rules

### Skills

Select the minimum useful skill set.

### Squads

Discover Squads through semantic analysis of the selected skill set:

1. Analyze skills for natural specialization clusters.
2. Define Squads around real specialization boundaries, not by name prefix, directory structure, or coincidental word overlap.
3. Each Squad must represent a coherent specialization, not merely an aggregation of skills.
4. Document each Squad with: identifier, name, mission, scope, capabilities, constraints, tags.

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
