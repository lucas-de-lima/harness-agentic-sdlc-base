# Discovery Output Validation

## Required Project Profile sections

- schema_version
- identity
- domain
- technical
- constraints
- risks
- open_questions

## Required identity

- proposed product name
- proposed repository name
- problem statement
- short description

## Required domain

- actors
- core concepts
- entities
- business rules

## Required technical

- application type
- persistence
- interfaces
- external dependencies

## Validation policy

Missing sections are failures.

Empty arrays are allowed when the evidence shows there is genuinely nothing identified.

Unknown or ambiguous behavior belongs in `open_questions` or `risks`; it must not be silently fabricated.
