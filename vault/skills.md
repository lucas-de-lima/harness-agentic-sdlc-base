---
id: skills
type: domain
aliases: [skills, abilities, capabilities]
tags: [base-harness, knowledge]
related:
  - id: _index
    relation: part_of
  - id: governance
    relation: governed_by
  - id: agents
    relation: used_by
  - id: workflows
    relation: triggered_by
canonical_doc: docs/SKILL_CATALOG.md
---

# Skills

Corpo de conhecimento e procedimento operacional para agentes.

## Famílias de skills base

| Família | Skills |
|---------|--------|
| Discovery | project-discovery, requirements-extraction, domain-modeling, project-naming |
| Architecture | architecture-evaluation, architecture-decision, adr-authoring, dependency-analysis |
| Go Engineering | idiomatic-go, go-project-structure, go-testing, go-http, go-concurrency |
| Infrastructure | docker-engineering, ci-engineering, database-integration |
| Quality | code-review, test-review, security-review, documentation-review |

## Ciclo de vida

`proposed → validated → active → deprecated`

## Especialização

[[docs/SKILL_SPECIALIZATION.md]]: Project Skills podem estender Base Skills com contexto de domínio, mas não podem contradizer políticas base.

## Relações

- [[skills]] são usadas por [[agents]]
- [[skills]] são acionadas por [[workflows]]
- [[skills]] seguem [[policies]]
- Project Skills (em [[docs/DEDICATED_HARNESS_SPECIFICATION.md|Dedicated Harness]]) herdam de Base Skills