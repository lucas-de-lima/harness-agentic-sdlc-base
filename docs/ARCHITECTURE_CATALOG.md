# Architecture Catalog

**Status:** v0.1
**Scope:** Harness Base and Dedicated Harnesses
**Purpose:** Provide a finite set of architecture candidates and selection rules for project-specific architecture decisions.

## 1. Principle

Architecture is selected to fit the system, not to demonstrate architectural sophistication.

The Architect Agent must prefer the simplest candidate that satisfies the system's known requirements, risks, operational constraints, and foreseeable evolution.

The catalog is a decision aid, not a mandatory menu. A project may use an architecture outside this catalog only when the need is explicit and the decision is recorded.

## 2. Candidate Architectures

### A1 — Simple Application

**Shape**

```text
cmd/
internal/
  application logic
  transport/adapters as needed
```

**Use when**

- the domain is small;
- there are few external integrations;
- most logic is straightforward;
- strong separation of domain/application/infrastructure would add ceremony without meaningful benefit.

**Typical characteristics**

- small number of packages;
- direct dependencies;
- standard library favored;
- minimal indirection.

**Main risk**

Logic can become tangled if the system grows beyond its original complexity.

---

### A2 — Layered Application

**Shape**

```text
Transport
   ↓
Application / Service
   ↓
Persistence / Infrastructure
```

**Use when**

- responsibilities naturally divide into a few technical layers;
- the application has moderate business logic;
- multiple handlers or entry points benefit from shared application logic;
- there is a meaningful persistence boundary.

**Main risk**

Layers can become artificial wrappers if every operation is forced through them.

---

### A3 — Modular Application

**Shape**

```text
Application
├── module A
├── module B
├── module C
└── shared infrastructure
```

**Use when**

- the system contains multiple coherent business capabilities;
- boundaries between capabilities are valuable;
- the application is still best deployed as one unit.

**Main risk**

Modules can become namespaces without real boundaries.

---

### A4 — Hexagonal / Ports and Adapters

**Shape**

```text
        adapters
      ↙    ↓     ↘
  HTTP   CLI   external API
      \    ↓    /
        ports
          ↓
    application/domain
```

**Use when**

- the domain/application logic should remain independent from infrastructure;
- multiple adapters or implementations are genuinely required;
- external integrations are significant;
- testing against infrastructure boundaries provides material value.

**Main risk**

Interfaces and adapters can become ceremony when there is only one simple implementation and little volatility.

---

### A5 — Modular Monolith

**Shape**

```text
Single deployable
├── bounded module A
├── bounded module B
├── bounded module C
└── shared technical infrastructure
```

**Use when**

- the domain has several strong boundaries;
- independent modules are valuable;
- independent deployment is not currently needed;
- a monolith keeps operations materially simpler than distributed services.

**Main risk**

False modularity or shared-state coupling can erase the intended boundaries.

---

### A6 — Event-Driven Component

**Shape**

```text
Producer → Event → Consumer(s)
```

This may exist inside a monolith or as part of a distributed system.

**Use when**

- asynchronous processing is a real business or operational requirement;
- loose temporal coupling provides value;
- event semantics are part of the problem;
- throughput or integration needs justify the added complexity.

**Main risk**

Operational complexity, eventual consistency, replay concerns, and harder debugging.

**Default stance**

Do not introduce event-driven architecture merely to demonstrate messaging technology.

---

### A7 — Distributed Services

**Shape**

```text
Service A ↔ Service B ↔ Service C
```

**Use only when**

- independent deployment is a concrete requirement;
- scaling isolation is materially valuable;
- ownership or organizational boundaries justify service separation;
- failure isolation provides a clear benefit;
- system boundaries are sufficiently understood.

**Main risk**

Distributed-system complexity: networking, retries, observability, deployment, contracts, consistency, and operational burden.

**Default stance**

Strongly disfavored for the portfolio projects unless the project requirements genuinely justify it.

---

## 3. Architecture Selection Order

The Architect Agent should evaluate candidates from simpler to more complex unless a requirement immediately eliminates the simpler choices.

Recommended default order:

```text
A1 Simple
  ↓
A2 Layered
  ↓
A3 Modular
  ↓
A4 Hexagonal
  ↓
A5 Modular Monolith
  ↓
A6 Event-Driven
  ↓
A7 Distributed Services
```

This is not an absolute complexity ranking. A small event-driven component can be simpler than a poorly designed layered system. The order is a deliberation heuristic.

## 4. Decision Dimensions

The Architect Agent evaluates at least these dimensions:

| Dimension | Question |
|---|---|
| Domain complexity | How much meaningful business logic exists? |
| Boundary complexity | Are there natural modules or bounded capabilities? |
| Integration complexity | How many external systems or adapters matter? |
| Persistence complexity | Is persistence simple or does it involve transactions, multiple stores, or significant data rules? |
| Concurrency | Is asynchronous or concurrent processing part of the real problem? |
| Deployment needs | Is one deployable unit sufficient? |
| Scaling needs | Is separate scaling materially useful? |
| Failure isolation | Is isolation between components a real requirement? |
| Change volatility | Which parts are likely to change independently? |
| Testing value | Do stronger boundaries provide meaningful testability benefits? |
| Operational burden | What infrastructure and debugging complexity does the architecture introduce? |

## 5. Decision Rule

The selected architecture must satisfy three conditions:

1. It satisfies known functional and non-functional requirements.
2. Its additional complexity has a concrete justification.
3. A simpler candidate was considered and rejected for a documented reason when the selected architecture is more complex than A1 or A2.

## 6. Required Architecture Output

The Architecture Decision artifact must contain:

- system summary;
- requirements relevant to architecture;
- candidate architectures considered;
- selected architecture;
- reasons for selection;
- rejected alternatives and reasons;
- major trade-offs;
- important risks;
- consequences;
- conditions that would justify revisiting the decision.

## 7. Architecture Escalation Rules

The Architect Agent must escalate complexity when evidence supports it.

Examples:

- A1 → A2 when shared application logic and technical boundaries become meaningful.
- A2 → A3 when multiple coherent business capabilities need explicit boundaries.
- A3 → A4 when infrastructure independence materially improves correctness, testing, or changeability.
- A3/A4 → A5 when module boundaries are strong but a single deployable remains operationally preferable.
- Any architecture → A6 when asynchronous/event semantics become a genuine system requirement.
- Any architecture → A7 only when distributed deployment or isolation has a concrete business/operational justification.

## 8. Forbidden Justifications

The following are not sufficient reasons to increase architectural complexity:

- "This is more enterprise."
- "This is a best practice."
- "Large companies use it."
- "It looks better on GitHub."
- "It demonstrates that I know the pattern."
- "AI agents work better with more layers."
- "We may need it someday."

## 9. Architecture Exceptions

A project may use an architecture outside the catalog when:

- an external constraint requires it;
- the domain presents a strong reason;
- a technology imposes a material architectural constraint;
- the catalog is demonstrably insufficient.

The exception requires an ADR explaining why the catalog was insufficient.

## 10. Definition of Done

The Architecture Catalog v0.1 is complete when:

- candidate architectures are finite and understandable;
- selection criteria are explicit;
- overengineering controls are explicit;
- the Architecture Decision output is defined;
- escalation rules are defined;
- exception handling is defined.
