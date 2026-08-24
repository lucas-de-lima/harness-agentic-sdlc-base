---
id: governance
type: domain
aliases: [governance, rules, constitution]
tags: [base-harness, foundation]
related:
  - id: _index
    relation: part_of
  - id: policies
    relation: empowers
  - id: architecture
    relation: governs
  - id: agents
    relation: governs
  - id: workflows
    relation: governs
canonical_doc: docs/HARNESS_BASE_CONSTITUTION.md
---

# Governance

O [[_index|Harness Base]] é governado pela **Constitution**.

## Documentos canônicos

- [[docs/HARNESS_BASE_CONSTITUTION.md]] — princípios, camadas, autoridade, conduta
- [[docs/HARNESS_TAXONOMY.md]] — unidades conceituais e relações
- [[docs/HARNESS_VERSIONING_MODEL.md]] — evolução independente
- [[docs/governance/CAPABILITY_OWNERSHIP.md]] — quem é dono do quê
- [[docs/governance/BASE_HARNESS_DOD.md]] — definition of done do Base

## Estrutura de autoridade

1. Constitution
2. [[policies]] obrigatórios
3. Arquitetura aprovada
4. ADRs
5. Implementação corrente
6. Preferência do agente (nunca silenciosa)

## Relações com outros domínios

- [[governance]] → [[policies]]: a Constituição estabelece as políticas obrigatórias
- [[governance]] → [[workflows]]: workflows devem respeitar quality gates e HITL
- [[governance]] → [[agents]]: agentes seguem conduta definida na Constitution