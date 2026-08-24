---
id: tools
type: domain
aliases: [tools, mcp, cli, ferramentas]
tags: [base-harness, execution]
related:
  - id: _index
    relation: part_of
  - id: governance
    relation: governed_by
  - id: agents
    relation: invoked_by
  - id: policies
    relation: restricted_by
canonical_doc: docs/MCP_TOOLING_ARCHITECTURE.md
---

# Tools

Capacidades externas disponíveis para agentes.

## Categorias

| Categoria | Exemplos | Acesso |
|-----------|----------|--------|
| Filesystem | Leitura/escrita de arquivos | Agent-scoped |
| Git | branch, commit, diff, log | Controlled |
| GitHub MCP | Issues, Projects, contexto | Read-only por padrão |
| GitHub CLI (gh) | PR view, merge, project edit | Controlled |
| Docker | Build, run, test | Go Engineer |
| harnessctl | Preflight, merge, HITL, branch-check, vault | Sempre disponível |

## Separação MCP vs gh CLI

- **MCP**: leitura de contexto, issues, projects fields
- **gh CLI**: operações de escrita (merge, project edit) e leitura adicional

Nunca assumir que todas as operações GitHub pertencem ao mesmo mecanismo.

## Autoridade de tools

[[docs/TOOL_AUTHORITY_MATRIX.md]] define por agente:

- Merge: **PROIBIDO** para todos os agentes
- Merge só via `harnessctl merge` (que valida HITL + identidade)
- Escrita GitHub: controlled por workflow

## Relações

- [[tools]] são invocadas por [[agents]]
- [[tools]] são restritas por [[policies]]
- [[tools]] operam dentro de [[workflows]]
- [[tools]] são governadas por [[governance]]