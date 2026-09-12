# Dedicated Harness Architecture

**Status:** Draft v0.1
**Scope:** Harness Base
**Applies to:** all Dedicated Harnesses generated from this base

## 1. Purpose

A Dedicated Harness specializes the Harness Base for one concrete domain.

The domain can be a technology stack, a professional discipline, a business area, a product type, a platform, an organization, or a combination.

The Base does not know the domain in advance. The Base teaches **how to build the specialization**, not what the specialization is.

## 2. The Specialization Problem

A Dedicated Harness may receive dozens, hundreds, or thousands of specialized resources:

- skills
- tools
- documentation
- procedures
- knowledge
- specialized agents
- workflows
- integrations

Exposing everything directly to the agent creates:

- excess context
- discovery difficulty
- selection difficulty
- higher cognitive load
- higher token consumption
- higher chance of selecting inadequate capabilities

A Dedicated Harness needs an intermediate specialization layer.

This layer is formed by **Squads**.

## 3. Squad Concept

A Squad is an operational context/specialization that an LLM agent can adopt to perform a specific role.

A Squad is not exclusively an agent. The same Squad context can be adopted by:

- main agent
- parallel agent
- background agent
- subagent

A single agent can change Squads during a task.

Mental model:

```
LLM   = actor
Squad = role/operational garment
Skills = capabilities available for that role
```

## 4. Squad Architecture

A Dedicated Harness can evolve to include:

```
Dedicated Harness
│
├── Squad Catalog
├── Squad Contexts
├── Skill Registry
├── Skills
├── Routing Rules
└── Agent Delegation Rules
```

### Squad Catalog

A registry of all available Squads in the Dedicated Harness. Each entry contains:

- identifier
- name
- mission
- scope
- capabilities
- constraints
- tags

The catalog is the discovery surface for LLM routing.

### Squad Contexts

The operational information an agent loads when adopting a Squad:

- mission
- scope
- capabilities
- constraints
- relevant resources
- operating rules

### Skill Registry

A structured index of all skills available in the Dedicated Harness. Each skill entry contains:

- id
- name
- summary
- domain
- capabilities
- tags

The full skill content is loaded only when the agent needs to execute the work.

### Skills

The actual skill files containing purpose, applicability, inputs, procedure, constraints, validation criteria, and failure modes.

### Routing Rules

Guidelines for how the LLM selects a Squad. The routing decision should be semantic, not mechanical.

### Agent Delegation Rules

Guidelines for how agents decompose work and delegate to subagents.

## 5. Bootstrap Process

The recommended sequence for building a Dedicated Harness:

```
Discover Domain
    ↓
Discover Available Capabilities
    ↓
Ingest Resources / Skills
    ↓
Summarize Resources
    ↓
Classify Capabilities
    ↓
Identify Natural Specializations
    ↓
Create Squads
    ↓
Build Registry
    ↓
Define Squad Contexts
    ↓
Define Routing
    ↓
Validate
```

This is a recommended process, not a rigid implementation.

## 6. Skill Ingestion

New skills can enter continuously. The process:

```
New Resource
    ↓
Inspect
    ↓
Generate concise summary
    ↓
Identify capabilities
    ↓
Identify domain/context
    ↓
Find appropriate Squad
    ↓
Register
    ↓
Validate
```

Works for both initial Dedicated creation and later evolution.

## 7. Discovery by Summary

A Dedicated Harness must not load the full content of all skills to discover relevance.

Initial discovery prefers compact metadata:

```
id
name
summary
domain
capabilities
tags
```

Full skill content loads only when needed for execution.

Goals:

- less context
- less token usage
- less latency
- better focus

## 8. Squad Organization

A Dedicated discovers its Squads through semantic analysis:

```
Skill collection
    ↓
semantic analysis
    ↓
natural clusters
    ↓
specialization boundaries
    ↓
Squads
```

Do not create Squads based solely on:

- skill count
- name prefix
- directory structure
- coincidental word overlap

Separation must represent real specialization.

## 9. On-Demand Squad Creation

When new skills enter:

```
New Skills
    ↓
Existing Squad adequate?
    ├── YES → associate with existing Squad
    └── NO
          ↓
      evaluate new specialization
          ↓
      create new Squad when justified
```

Do not create new Squads automatically for any difference. A new Squad must represent a coherent new specialization.

## 10. LLM-Native Routing

The semantic routing decision should be made by the LLM whenever possible.

```
User Request
    ↓
LLM understands request
    ↓
reads Squad Catalog
    ↓
selects appropriate Squad
    ↓
adopts Squad Context
    ↓
discovers relevant Skills
    ↓
executes
```

Avoid turning routing into a rigid classifier based on:

- keywords
- regex
- arbitrary scores
- aliases
- artificial thresholds

Code may exist for mechanical and deterministic functions. Semantic understanding should remain with the LLM.

## 11. What Before How

First determine **what the user is trying to achieve**, then determine **how it will be done**.

The technical domain mentioned in the request should not automatically determine the role the agent adopts.

A request may relate to a technology but still be in a stage of:

- discovery
- planning
- design
- evaluation
- decision making

The Harness must identify the current nature of the work before choosing the operational specialization.

## 12. Squad Adoption

After selecting a Squad:

```
LLM
    ↓
adopts Squad Context
    ↓
operates according to that specialization
    ↓
discovers relevant skills
    ↓
executes
```

Squad adoption loads:

- mission
- scope
- capabilities
- constraints
- context
- relevant resources
- operating rules

A Squad is operational context, not necessarily a separate process.

## 13. Agent Delegation

The main agent should delegate isolatable work to subagents when it brings advantages in:

- parallelism
- context isolation
- load reduction
- independent investigation
- lower blocking risk
- better specialization

Flow:

```
Main Agent
    ↓
decompose task
    ↓
create subagent(s)
    ↓
each subagent adopts appropriate Squad
    ↓
subagents execute
    ↓
Main Agent consumes results
    ↓
Main Agent integrates result
```

The main agent remains responsible for coordination.

## 14. Subagent Specialization

A subagent does not automatically inherit the same specialization as the main agent.

Conceptual example:

```
Main Agent
  → Squad A

Subagent 1
  → Squad B

Subagent 2
  → Squad C
```

This is expected behavior in multi-specialty tasks. Each agent should have context appropriate to the work it is actually performing.

## 15. Timeout and Failure Isolation

A subagent must not block the main agent indefinitely.

Basic states:

```
started
completed
failed
timed_out
```

When timeout is reached and state becomes `timed_out`, the main agent must remain able to:

- evaluate the result
- retry when appropriate
- recreate the subagent
- re-divide the task
- proceed by another path
- conclude with partial information

A blocked subagent must not mean the entire Harness is blocked.

## 16. Harness as Orchestrator

The main agent should act primarily as:

```
planner
orchestrator
supervisor
integrator
decision maker
```

When an operational task can be safely isolated, consider delegating it.

Do not treat this as absolute dogma. The decision should consider:

- complexity
- duration
- independence
- risk
- delegation cost
- parallelism benefit

## 17. Knowledge Source vs Decision Mechanism

Separation of concerns:

```
MD / YAML / Registry
        ↓
knowledge + structure + context

LLM
        ↓
semantic understanding + selection + reasoning + execution

Code
        ↓
deterministic infrastructure
```

Do not create code merely to replace a capability the LLM can exercise better through well-structured context.

## 18. Continuous Evolution

The Dedicated Harness is a living system. New capabilities can appear at any time.

```
new resource
    ↓
ingest
    ↓
classify
    ↓
associate with existing Squad
    OR
create justified new Squad
    ↓
update registry/context
    ↓
validate
```

Do not assume the initial taxonomy will remain perfect forever.

## 19. Bootstrap vs Implementation

### Harness Base

Defines:

```
principles
process
architecture
rules
generic mechanisms
```

### Dedicated Harness

Defines:

```
domain
skills
Squads
contexts
capabilities
vocabulary
tools
integrations
```

The Base must never try to decide in advance what specializations a Dedicated will have.