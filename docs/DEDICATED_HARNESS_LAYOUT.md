# Dedicated Harness Layout

## Purpose

Define the first concrete `.harness` layout for product repositories.

```text
.harness/
├── README.md
├── manifest.yaml
├── project-profile.md
├── architecture.md
├── context/
│   ├── domain.md
│   └── vocabulary.md
├── squads/
│   ├── catalog.yaml
│   └── contexts/
├── agents/
├── skills/
├── policies/
├── workflows/
└── tools/
```

## manifest.yaml

The manifest identifies:

- harness version
- Base Harness version
- project identifier
- architecture profile
- selected skills
- selected Squads
- selected agents
- selected tools
- enabled workflows

The manifest is metadata, not executable agent logic.

## Agents

Only project-specific configuration belongs here.

## Squads

Project-specific Squad definitions live here. Each Squad entry in the catalog references the skills relevant to its specialization. The Squad contexts directory holds the operational information agents load when adopting a Squad.

## Skills

Project overlays live here. Base skills remain owned by the Base Harness.

## Policies

Project-specific constraints that tighten or clarify Base rules.

## Workflows

Project lifecycle or task-specific orchestration definitions.

## Tools

Project-specific tool configuration and least-privilege capability selection.
