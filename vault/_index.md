---
id: _index
type: root
aliases: [home, index, entry]
tags: [vault, base-harness]
related:
  - id: governance
    relation: contains
  - id: architecture
    relation: contains
  - id: agents
    relation: contains
  - id: skills
    relation: contains
  - id: workflows
    relation: contains
  - id: policies
    relation: contains
  - id: tools
    relation: contains
canonical_doc: docs/HARNESS_BASE_CONSTITUTION.md
---

# Harness Base Vault

Este vault contém o grafo de conhecimento do [[governance|Harness Base]].

## Domínios

| Nota | Propósito |
|------|-----------|
| [[governance]] | Constituição, taxonomia, lifecycle, ownership |
| [[architecture]] | Catálogo de arquiteturas, padrões, decisões |
| [[agents]] | Roles, autoridade, responsabilidades |
| [[skills]] | Catálogo de skills, especialização |
| [[workflows]] | Catálogo de workflows, estados, transições |
| [[policies]] | Branching, HITL, identidade, bootstrap |
| [[tools]] | MCP, CLI, ferramentas de autoridade |

## Princípios base

- [[governance]] governa todos os outros domínios
- [[architecture]] seleciona a estrutura do sistema
- [[agents]] usam [[skills]] e [[tools]]
- [[workflows]] orquestram [[agents]], [[skills]] e [[policies]]
- [[policies]] restringem [[agents]] e [[workflows]]
- [[tools]] são invocados por [[agents]] dentro de [[policies]]

## Consulta

```sh
harnessctl vault query --find <term>
harnessctl vault query --follow <id>
harnessctl vault query --graph
harnessctl vault validate
```