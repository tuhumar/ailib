# Repository status matrix

This document is the current source-of-truth summary for the public repository state.

Its purpose is simple:

- clarify what is **present in the repository now**
- distinguish between **observed implementation**, **documented intent**, and **future roadmap work**
- reduce ambiguity for contributors and users

This file should be updated whenever public docs, packaging metadata, examples, or API exports change materially.

---

## Status legend

- **implemented** — visible in the current public repository and intended for use
- **partial** — present, but not yet fully aligned, hardened, or proven by docs/tests/CI
- **documented target** — described in docs/changelog, but still needs verification or completion
- **planned** — not claimed as current functionality; belongs to roadmap/backlog work

---

## Current repository assessment

### 1. Public library shape

| Capability | Current status | Notes |
|---|---|---|
| Top-level package exports in `ailib.__init__` | partial | Public API surface is broad and suggests a more mature architecture than a minimal MVP. |
| Explicit `Client` API | implemented | Present in the public source tree and clearly intended as a core abstraction. |
| Global context helpers (`get_client`, `set_client`, `set_backend`, `reset_context`, `use_backend`) | implemented | Present and usable; should continue to be documented as the convenience layer. |
| Legacy/simple `core.py` style entry points | partial | Repository still appears to contain older/simple patterns alongside newer modular architecture. |

### 2. Backends and transport

| Capability | Current status | Notes |
|---|---|---|
| `stdio` / `stdin` backend flow | partial | Public docs describe robust stdio support; implementation and validation need to stay aligned. |
| `file` backend flow | partial | Public docs describe request/response file workflows; durable hardening remains roadmap work. |
| Transport-agnostic interruption contract | documented target | Public docs point in this direction, but protocol tightening remains active roadmap work. |

### 3. Structured response handling

| Capability | Current status | Notes |
|---|---|---|
| `ask_json()` | implemented | Present and part of public API. |
| model-based structured parsing (`ask_model`) | implemented | Present in public API, with optional dependency expectations. |
| local schema validation | partial | Documented and directionally present, but still part of the area that needs protocol/validation hardening over time. |

### 4. Protocol and lifecycle semantics

| Capability | Current status | Notes |
|---|---|---|
| request/response envelope direction | documented target | README/changelog describe explicit envelope-based architecture. |
| stable interruption / approval / resume semantics | planned | This is now a core roadmap direction, but should not yet be treated as fully shipped category-leading behavior. |
| durable resume and checkpoint lineage | planned | Explicit roadmap work. |
| replay / fork / operator inbox / policy engine | planned | Explicit roadmap work, not current product state. |

### 5. Observability and operator tooling

| Capability | Current status | Notes |
|---|---|---|
| transcript model | documented target | Discussed in roadmap/backlog direction; should not yet be framed as fully shipped unless validated in code/docs/tests together. |
| OpenTelemetry-style lifecycle hooks | planned | Roadmap item. |
| host CLI / operator tools | planned | Roadmap item. |
| TUI / inbox / approval bridges | planned | Roadmap item. |

### 6. Packaging and release discipline

| Capability | Current status | Notes |
|---|---|---|
| package metadata and build system | implemented | `pyproject.toml` is present and defines package metadata/build backend. |
| coherent release/version narrative | partial | The repository currently presents a mature version line, while roadmap work still includes foundational alignment tasks. |
| CI as trusted source of package health | documented target | Public docs refer to CI, but contributors should verify root-level workflow wiring and green status. |

---

## Contributor guidance

### Treat these as the current stable orientation

- `Client` plus context helpers are the public shape to preserve.
- `ask`, `decide`, `ask_json`, and `ask_model` are part of the intended user-facing API.
- `stdio` and `file` transport patterns are part of the project direction and should be kept working/documented carefully.

### Treat these as active alignment areas

- versioning / release narrative
- exact protocol maturity claims
- CI and validation discipline
- distinction between current behavior and roadmap ambition

### Treat these as roadmap-only unless explicitly implemented and documented

- world-class interruption / approval / resume lifecycle
- durable cross-process checkpointing and replay
- lineage graphs and time travel
- policy engine hooks
- operator inboxes, TUI, bridges, and ecosystem adapters

---

## Near-term maintenance rule

Whenever one of the following changes, update this file in the same PR:

- public exports
- README claims
- package versioning policy
- CI/build policy
- roadmap status of a capability that moves from planned to implemented

This keeps the repository honest and keeps the roadmap anchored to the real codebase.
