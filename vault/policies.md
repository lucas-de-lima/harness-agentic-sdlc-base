---
id: policies
type: domain
aliases: [policies, rules, constraints]
tags: [base-harness, governance]
related:
  - id: _index
    relation: part_of
  - id: governance
    relation: derived_from
  - id: agents
    relation: constrains
  - id: workflows
    relation: enforces
  - id: tools
    relation: restricts
canonical_doc: docs/HITL_POLICY.md
---

# Policies

Restrições obrigatórias que todo Dedicated Harness deve respeitar.

## Políticas base

| Política | Propósito | Documento |
|----------|-----------|-----------|
| Branching | main → develop → feature/ → story/ | [[docs/BRANCHING_POLICY.md]] |
| HITL | Humanos aprovam merge, release, arquitetura | [[docs/HITL_POLICY.md]] |
| Identidade GitHub | Nunca inferir owner/repo do path local | [[docs/GITHUB_IDENTITY_GUARDRAIL.md]] |
| Bootstrap | Preflight + gitignore antes do primeiro push | [[docs/REPOSITORY_BOOTSTRAP_RULES.md]] |

## HITL Gates obrigatórios

| Gate | Trigger |
|------|---------|
| HG-PRODUCT | Decisão de produto/escopo |
| HG-ARCHITECTURE | Mudança material de arquitetura |
| HG-MERGE-STORY | Merge story → feature |
| HG-MERGE-FEATURE | Merge feature → develop |
| HG-MERGE-DEVELOP | Merge develop → main |
| HG-RELEASE | Release/tag |
| HG-SECURITY-EXCEPTION | Exceção de segurança |

## Herança

Um Dedicated Harness **herda** todas as políticas do Base.
Pode **apertar** regras, mas **não pode enfraquecer** políticas obrigatórias.

## Relações

- [[policies]] derivam de [[governance]]
- [[policies]] constrangem [[agents]]
- [[policies]] são aplicadas por [[workflows]]
- [[policies]] restringem acesso a [[tools]]