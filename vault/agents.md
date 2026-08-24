---
id: agents
type: domain
aliases: [agents, roles, agent-roles]
tags: [base-harness, orchestration]
related:
  - id: _index
    relation: part_of
  - id: governance
    relation: governed_by
  - id: skills
    relation: uses
  - id: workflows
    relation: participates_in
  - id: policies
    relation: constrained_by
  - id: tools
    relation: invokes
canonical_doc: docs/AGENT_SPECIFICATION.md
---

# Agents

Roles com responsabilidade por decisões e execução.

## Agentes base

| Agent | Responsabilidade |
|-------|----------------|
| Orchestrator | Fluxo, estado, transições |
| Discovery | Descoberta de projeto legado |
| Architect | Decisão de arquitetura |
| Planner | Breakdown de trabalho |
| Engineer | Implementação |

## Autoridade (AGENT_AUTHORITY_MATRIX)

| Role | Implementa | Revisa | Merge |
|------|-----------|--------|-------|
| Orchestrator | Não | Não | **PROIBIDO** |
| Discovery | Não | Não | **PROIBIDO** |
| Architect | Design | Sim | **PROIBIDO** |
| Engineer | Sim | Não | **PROIBIDO** |
| Reviewer | Não | Sim | **PROIBIDO** |

Nenhum agent faz merge diretamente. Merge é sempre via [[tools|harnessctl merge]] com gate HITL.

## Relações

- [[agents]] usam [[skills]] para executar trabalho
- [[agents]] invocam [[tools]] (MCP, CLI)
- [[agents]] são governados por [[governance]]
- [[agents]] seguem [[policies]] (branching, HITL, identidade)
- [[agents]] participam de [[workflows]]