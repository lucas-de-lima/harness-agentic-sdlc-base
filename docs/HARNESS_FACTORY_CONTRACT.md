# Harness Factory Contract

## Factory responsibilities

The Factory must:

- inspect the project
- build the Project Profile
- deliberate on naming
- select architecture
- select relevant capabilities
- discover Squads from the selected capabilities
- generate the Dedicated Harness with Squad structure
- validate the generated harness
- report unresolved decisions

## Factory must not

- implement the application itself
- bypass architecture deliberation
- hide unresolved ambiguity
- introduce arbitrary global standards
- mutate unrelated repositories
- create unnecessary capabilities

## Validation

Generation is successful only when:

- required files exist
- configuration is internally consistent
- Squads are coherent (each represents a real specialization)
- selected agents have needed skills for their assigned Squads
- selected tools satisfy permissions
- workflow references valid states
- project-specific policies do not conflict with Base Constitution
- unresolved blocking questions are explicitly surfaced

## Human intervention

Human input is required when a decision is consequential and evidence is insufficient for safe autonomous selection.
