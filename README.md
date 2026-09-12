# Agentic SDLC Base

Harness Base generico e independente de dominio usado como fundacao para criar Dedicated Harnesses para projetos especificos.

## Arquitetura

```
Harness Base
    ↓
Dedicated Harness
    ↓
System
```

- **Harness Base** — principios, processos, arquitetura, regras, mecanismos reutilizaveis
- **Dedicated Harness** — especializacao para um dominio concreto com skills, Squads, contextos, ferramentas
- **System** — produto de software sendo construido

## Conceito Central: Squad

Squad e identidade/contexto operacional que um agente LLM adota para desempenhar um papel.

```
LLM = ator
Squad = personagem/vestimenta operacional
Skills = capacidades disponiveis para aquele papel
```

Um Squad pode ser adotado por agente principal, agente paralelo, subagente.
Um mesmo agente muda de Squad durante tarefa.

## Documentacao Principal

| Documento | Conteudo |
|---|---|
| `docs/HARNESS_BASE_CONSTITUTION.md` | Principios, regras, autoridade, politicas |
| `docs/HARNESS_TAXONOMY.md` | Unidades conceituais: Requirement → Skill → Squad → Agent → Tool → Workflow |
| `docs/DEDICATED_HARNESS_ARCHITECTURE.md` | Squad, bootstrap, routing, delegacao, timeout, evolucao |
| `docs/DEDICATED_HARNESS_SPECIFICATION.md` | Estrutura esperada de um Dedicated Harness |
| `docs/DEDICATED_HARNESS_LAYOUT.md` | Layout concreto `.harness/` |
| `docs/HARNESS_GENERATION_RULES.md` | Ordem de geracao, regras de selecao |
| `docs/HARNESS_FACTORY_CONTRACT.md` | Responsabilidades da Harness Factory |

## Skills Canonica

`skills/base/` contem skills reutilizaveis entre projetos.

## Uso

```bash
# Validar repositorio base
make validate

# Executar testes
make test

# Inspecionar projeto real para criar Dedicated Harness
python scripts/inspect_real_project.py --project /caminho/do/projeto --output /tmp/discovery
```

## Status

Phase 31 — Real Project Discovery: pronto para execucao.
Primeira fase que opera sobre repositorios reais de projeto.

Nenhum arquivo de producao deve ser modificado durante descoberta.