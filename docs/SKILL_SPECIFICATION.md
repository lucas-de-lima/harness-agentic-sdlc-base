# Skill Specification

## Purpose

A Skill is a bounded, reusable capability instruction set used by agents.

A skill MUST:
- have one clear responsibility;
- define when it applies;
- define required inputs/context;
- define expected outputs;
- define validation expectations;
- avoid owning orchestration.

A skill MUST NOT:
- decide overall project architecture unless explicitly scoped as an architecture skill;
- silently change project policy;
- duplicate another skill's responsibility;
- encode project-specific assumptions inside a Base Skill.

## Required Metadata

Every skill must declare:

- `id`
- `name`
- `version`
- `scope` (`base` or `project`)
- `purpose`
- `triggers`
- `inputs`
- `outputs`
- `dependencies`
- `validation`
- `forbidden_behaviors`

## Composition

Skills compose through context, not inheritance.

A Project Skill may:
- add domain-specific knowledge;
- narrow a Base Skill's applicability;
- add project-specific validation;
- add project-specific examples.

A Project Skill may NOT silently contradict a Base policy.

## Skill Quality Test

A skill is ready when:
1. Its responsibility can be stated in one sentence.
2. Its trigger conditions are observable.
3. Its inputs are explicit.
4. Its outputs are inspectable.
5. Its validation is executable or reviewable.
6. It has no unnecessary overlap with another skill.
