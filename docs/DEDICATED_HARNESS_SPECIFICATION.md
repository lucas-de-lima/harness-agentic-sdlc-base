# Dedicated Harness Specification

## Purpose

Define the structure and responsibilities of a project-specific harness.

## Proposed repository structure

```text
.harness/
├── README.md
├── project-profile.md
├── architecture.md
├── agents/
├── skills/
├── policies/
├── workflows/
├── tools/
└── context/
```

This is a conceptual structure. Exact file formats may evolve during implementation.

## Required contents

### README

Explains how the Dedicated Harness differs from the Base Harness and how to operate it.

### Project Profile

The approved discovery model.

### Architecture

The selected architecture and rationale.

### Agents

Only project-relevant agent configuration.

### Skills

Project-specific skills and specialization overlays.

### Policies

Project-specific constraints and quality requirements.

### Workflows

Project-specific lifecycle workflows.

### Tools

Tool configuration and capability restrictions.

### Context

Durable domain vocabulary and project knowledge required by agents.

## HITL inheritance

A Dedicated Harness inherits the HITL policy from the Base Harness (see `HITL_POLICY.md`).
It may materialize:

- which mandatory gates are applicable (all apply unless a workflow is genuinely unused,
  e.g., no release step → `HG-RELEASE` marked not-applicable with justification);
- who the approver is, when configurable (`expected_authority`);
- additional project-specific gates.

A Dedicated Harness **cannot remove a mandatory Human Gate** from the Base. Use
`harnessctl hitl validate <project-root>` to check that no mandatory gate has been
disabled.
