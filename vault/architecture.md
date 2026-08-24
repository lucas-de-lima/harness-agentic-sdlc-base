---
id: architecture
type: domain
aliases: [architecture, arch, adr]
tags: [base-harness, design]
related:
  - id: _index
    relation: part_of
  - id: governance
    relation: governed_by
  - id: skills
    relation: uses
  - id: agents
    relation: decided_by
canonical_doc: docs/ARCHITECTURE_CATALOG.md
---

# Architecture

Catálogo de arquiteturas candidatas e padrões reutilizáveis.

## Documentos canônicos

- [[docs/ARCHITECTURE_CATALOG.md]] — 7 arquiteturas candidatas (A1–A7)
- [[docs/PATTERN_CATALOG.md]] — 16 padrões de design
- [[docs/ARCHITECTURE_DECISION_FRAMEWORK.md]] — como decidir
- [[docs/ADR_TEMPLATE.md]] — template de ADR

## Arquiteturas candidatas (da mais simples à mais complexa)

| ID | Nome | Uso típico |
|----|------|------------|
| A1 | Simple | Domínio pequeno, poucas integrações |
| A2 | Layered | Separação técnica moderada |
| A3 | Modular | Capacidades de negócio coerentes |
| A4 | Hexagonal | Independência de infraestrutura |
| A5 | Modular Monolith | Módulos fortes, single deploy |
| A6 | Event-Driven | Processamento assíncrono real |
| A7 | Distributed | Deployment/isolamento independente |

## Decisões de arquitetura

Toda decisão material requer:

1. [[docs/ARCHITECTURE_DECISION_FRAMEWORK.md|Deliberação]] pelo [[agents|Architecture Agent]]
2. ADR documentado
3. Aprovação humana (HG-ARCHITECTURE via [[policies|HITL policy]])

## Relações

- [[architecture]] usa [[skills|architecture-deliberation skill]]
- [[architecture]] é decidida por [[agents|architect agent]]
- [[architecture]] alimenta [[workflows|WF-002 Architecture Deliberation]]
- [[architecture]] é governada por [[governance]]