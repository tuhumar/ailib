# Repository status matrix

This document is the current source-of-truth summary for the public repository state.

## Status legend

- **implemented** — visible in the current public repository and intended for use
- **partial** — present, but not yet fully aligned, hardened, or proven by docs/tests/CI
- **documented target** — described in docs/changelog, but still needs verification or completion
- **planned** — belongs to roadmap/backlog work and is not yet a baseline guarantee

## Current repository assessment

### Public library shape
- `Client` API: implemented
- global context helpers (`get_client`, `set_client`, `set_backend`, `reset_context`, `use_backend`): implemented
- top-level convenience API (`ask`, `decide`, `ask_json`, `ask_model`): implemented
- legacy/simple entry-point patterns coexisting with newer modular architecture: partial

### Backends and transport
- `stdio` / `stdin` backend flow: partial
- `file` backend flow: partial
- transport-agnostic interruption contract: documented target

### Structured response handling
- `ask_json()`: implemented
- `ask_model()`: implemented
- local schema/model validation story: partial

### Protocol and lifecycle semantics
- request/response envelope direction: implemented directionally
- stable interruption / approval / resume semantics: planned
- durable checkpointing, replay, lineage, operator inbox, policy engine: planned

### Observability and operator tooling
- transcript model direction: documented target
- OpenTelemetry hooks: planned
- host CLI and operator tools: planned
- TUI / inbox / approval bridges: planned

### Packaging and release discipline
- package metadata and build system: implemented
- coherent release/version narrative: partial
- CI as trusted package health source: partial but improving

## Contributor guidance

Treat these as current stable orientation:
- `Client` plus context helpers
- `ask`, `decide`, `ask_json`, `ask_model`
- `stdio` and `file` transport patterns as active supported directions

Treat these as active alignment areas:
- versioning / release narrative
- protocol maturity claims
- CI and validation discipline
- distinction between shipped behavior and roadmap ambition

Treat these as roadmap-only unless explicitly implemented and documented:
- world-class interruption / approval / resume lifecycle
- durable cross-process checkpointing and replay
- lineage graphs and time travel
- policy engine hooks
- operator inboxes, TUI, bridges, and ecosystem adapters
