---
id: workflows
type: domain
aliases: [workflows, wf, processos]
tags: [base-harness, orchestration]
related:
  - id: _index
    relation: part_of
  - id: governance
    relation: governed_by
  - id: agents
    relation: assigns
  - id: skills
    relation: triggers
  - id: policies
    relation: constrained_by
canonical_doc: docs/WORKFLOW_CATALOG.md
---

# Workflows

Sequências orquestradas de atividades, decisões e handoffs.

## Workflows base

| ID | Nome | Agent | Input → Output |
|----|------|-------|----------------|
| WF-001 | Project Discovery | discovery | spec → Profile |
| WF-002 | Architecture Deliberation | architect | Profile → ADR |
| WF-003 | Harness Generation | factory | Profile → Harness |
| WF-004 | Implementation Planning | planner | Architecture → Backlog |
| WF-005 | Implementation | go-engineer | Feature → Code + Tests |
| WF-006 | Code Review | reviewer | Code → Approval |
| WF-007 | Release | release-reviewer | Develop → Release |

## Estados

`Backlog → Ready → In Progress → In Review → Done`

Qualquer estado pode ir para `Blocked`.

## Máquina de estados

Ver [[docs/WORKFLOW_STATE_MACHINE.md]] para transições控制adas.

## Guardrails

- Toda execução é bounded (max_attempts)
- Merge exige HITL gate
- Review é independente do implementador
- Agente não aprova o próprio trabalho

## Relações

- [[workflows]] atribuem [[agents]]
- [[workflows]] acionam [[skills]]
- [[workflows]] seguem [[policies]]
- [[workflows]] são governados por [[governance]]