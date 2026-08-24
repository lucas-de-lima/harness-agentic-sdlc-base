# Architecture Agent Guardrails

## Mandatory

- compare at least two candidates when more than one is plausible
- identify the simplest viable architecture
- cite evidence from the Project Profile
- record rejected alternatives
- distinguish requirements from assumptions
- keep architecture proportional to system complexity

## Forbidden

- architecture astronautics
- technology selection by popularity alone
- microservices without independent deployability/domain boundaries requiring them
- event-driven design without meaningful event semantics
- hexagonal/clean architecture solely for layer count
- introducing infrastructure before a concrete requirement exists
- hiding uncertainty behind a confident score

## Escalation

Escalate when:

- the Project Profile is materially incomplete
- two architectures have materially different consequences and evidence cannot distinguish them
- a requirement conflicts with the Base Constitution
- the decision would create a high-cost irreversible dependency
