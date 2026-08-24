# Agent Instruction Layering

## Purpose

Define how durable instructions are layered without creating conflicting copies of the same rule.

## Instruction hierarchy

```text
Base Constitution
        ↓
Base capability/role rules
        ↓
Project Harness policies
        ↓
Task-specific instructions
        ↓
Execution evidence
```

Higher-level rules remain authoritative unless the system explicitly permits specialization.

## Repository-native instructions

The implementation should use the instruction mechanism supported by the selected agent runtime. For Codex, the runtime-specific repository instruction mechanism should be validated at implementation time rather than hard-coded prematurely.

## Principle

Instruction files are for behavioral constraints and context.

They should not contain:

- live backlog state
- copied source code
- long transient plans
- duplicated architecture decisions

## Conflict handling

If two instructions conflict:

1. identify both
2. determine their authority level
3. apply the higher-authority rule
4. surface the conflict if it changes behavior materially
5. never silently choose a weaker safety constraint
