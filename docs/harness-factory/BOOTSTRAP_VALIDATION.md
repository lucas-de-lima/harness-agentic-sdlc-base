# Dedicated Harness Validation

## Structural

Require:

- `.harness/README.md`
- `.harness/manifest.yaml` or `.json`
- `.harness/project-profile.md`
- `.harness/architecture.md`
- enabled agent configuration
- enabled skill references
- applicable policies
- workflow references

## Consistency

Validate:

- Base version present
- architecture matches approved decision
- every enabled workflow has required skills
- every enabled agent has allowed capabilities
- selected tools satisfy permissions
- no project policy weakens Base Constitution

## Safety

Before generation completes:

- no production source should be modified
- no dependency should be added
- no GitHub mutation should occur
- no generated file should contain secrets
