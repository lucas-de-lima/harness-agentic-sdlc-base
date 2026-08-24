# Harness Factory Architecture

## Purpose

The Harness Factory turns a legacy project specification into a Dedicated Harness.

The Base Harness does not become the project harness itself. It provides the rules, templates, catalogs, and generation process used to specialize a project.

## Flow

```text
Legacy specification
        ↓
Discovery
        ↓
Project Profile
        ↓
Architecture Decision
        ↓
Capability selection
        ↓
Agent selection
        ↓
Tool selection
        ↓
Policy specialization
        ↓
Dedicated Harness
```

## Core principle

The Factory generates configuration and context from approved Base capabilities.

It must not silently invent new global rules.

## Inputs

- original project `.md`
- available legacy source files, when present
- Base Harness catalogs
- approved architecture framework
- project constraints
- project-specific requirements

## Outputs

- Project Profile
- Project Naming Decision
- Architecture Decision
- Dedicated Harness
- initial GitHub Project bootstrap specification
- unresolved questions/risk register

## Specialization boundary

The Dedicated Harness may specialize:

- context
- vocabulary
- skills
- agent prompts/configuration
- tool access
- workflow constraints
- quality gates

It may not weaken Base Constitution rules unless a future Base-level governance process explicitly authorizes an exception.
