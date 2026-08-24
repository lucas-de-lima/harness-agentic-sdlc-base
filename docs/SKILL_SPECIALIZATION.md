# Skill Specialization Model

## Objective

Allow a Dedicated Harness to specialize Base Skills without copying or mutating the Base Skill.

## Model

```text
Base Skill
   +
Project Context
   +
Project Skill (optional)
   =
Effective Capability
```

## Allowed Specialization

A project-level skill may:
- constrain scope;
- add domain terminology;
- add domain rules;
- add project-specific examples;
- add validation;
- add known failure modes.

## Not Allowed

A project-level skill may not:
- weaken a Base policy;
- redefine security requirements;
- silently change architecture decisions;
- duplicate the full Base Skill;
- create global assumptions from local behavior.

## Conflict Resolution

Priority:

1. Base Constitution
2. Base Quality/Safety Policy
3. Project Architecture Decision
4. Project Policies
5. Project Skills
6. Base Skills
7. Agent task instructions

When two skills conflict at the same level, the Orchestrator must stop and request deliberation instead of arbitrarily choosing.

## Example

Base:
`go-http`

Project:
`project-payments-http`

The project skill can specify:
- required endpoints;
- domain error mapping;
- authentication assumptions;
- response conventions.

It does not redefine what idiomatic Go means globally.
