# Codex Instruction Contract

## Purpose

Define the minimum contract for repository instructions consumed by Codex.

## Required behavior

An instruction file must:

- identify the repository/layer
- define applicable boundaries
- point to durable governing documents
- state prohibited shortcuts
- explain validation commands
- remain concise enough to be practical

## Instruction hierarchy

```text
System/developer/user instructions
        ↓
Higher-scope AGENTS.md
        ↓
Lower-scope AGENTS.md
        ↓
Task-specific skill
        ↓
Current work item
```

Direct higher-priority instructions override repository instructions.

Codex applies deeper `AGENTS.md` files to files within their directory scope. citeturn817121search1turn817121search10

## Rule

Do not copy the whole Base Constitution into every project instruction file.

Reference the governing document and state only project-specific rules that the agent needs operationally.
