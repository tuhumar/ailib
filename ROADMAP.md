# ailib Roadmap

## Purpose

This roadmap turns `ailib` from a useful but still transitional agent-interruption MVP into a stable, documented, release-ready library for agent-in-the-loop execution.

It is intentionally ambitious. The repository already shows two important signals:

1. the visible package code is still centered around a small API surface (`ask`, `ask_json`, `decide`, `set_backend`, `use_backend`) with two concrete transports (`StdinBackend`, `FileBackend`);
2. the project documentation already points toward a richer target state: explicit request/response envelopes, stronger typing, host-side helpers, optional schema validation, CI, examples, and cleaner release hygiene.

The roadmap therefore does **not** assume that the project is already fully in that target state. Instead, it treats the current situation as a **transition period** and makes “repository truth alignment” the first milestone.

---

## Product Vision

`ailib` should become the minimal but robust Python standard layer for **supervised AI execution**:

- a running script can pause and ask a supervising agent for input;
- the request is serialized in a predictable, machine-readable format;
- the supervising host can respond through different transports;
- application code gets a clean public API with strong errors, typed validation, and deterministic behavior;
- the library stays lightweight enough for embedding inside tools, agents, wrappers, runners, CLIs, and automation pipelines.

### Core promise

> "When an AI-driven process needs help, `ailib` makes the interruption explicit, structured, transport-agnostic, testable, and safe to automate."

---

## Non-goals

These are intentionally out of scope unless the project later decides otherwise:

- turning `ailib` into a full agent framework;
- bundling model inference providers directly into the core library;
- owning business logic for specific applications;
- forcing async/event-loop complexity into the default happy path;
- becoming a heavy RPC stack when a smaller interruption protocol is enough.

---

## Current-State Assessment

### What is already valuable

- Simple, understandable public API.
- Two immediately useful backends (`stdin`/`file`).
- Environment-variable-based backend selection.
- Basic timeout support in file mode.
- JSON extraction convenience in `ask_json()`.
- A small test suite demonstrating intended behavior.
- Documentation that already sketches a more mature architecture.

### Main risks observed

1. **Repository truth drift**
   - Public code, packaging metadata, README, CONTRIBUTING, and changelog appear to describe different maturity levels.
   - This is the single highest-priority problem because users cannot trust contracts if docs and code diverge.

2. **Protocol ambiguity**
   - The MVP request/response shape is lightweight, but the project needs a canonical envelope to support compatibility, structured errors, and future transports.

3. **Transport fragility**
   - `stdin` and polling files are enough for experimentation, but they need stronger cleanup, matching, framing, and failure semantics for real automation.

4. **Release ambiguity**
   - The project needs a single canonical versioning story, reproducible builds, CI, and a PyPI publication path.

5. **Validation gap**
   - `ask_json()` is useful, but production use needs explicit schema/model validation with predictable exceptions.

6. **DX and host integration gap**
   - The supervising side of the protocol needs first-class helpers and reference integrations for Codex/GPT/Gemini/Claude-style host runtimes.

---

## Roadmap Principles

1. **Source of truth first** — no new features before code/docs/version alignment.
2. **Small public API, strong internals** — keep the surface simple, but make the protocol and errors rigorous.
3. **Backward compatibility by policy** — compatibility must be explicit and tested, not accidental.
4. **Transport-agnostic core** — protocol and validation should not depend on a single backend.
5. **Host ergonomics matter** — the supervisor side is part of the product, not an afterthought.
6. **Release discipline over feature sprawl** — CI, versioning, changelog, packaging, and examples must evolve with the code.
7. **Typed where it matters** — models, exceptions, envelopes, and validation paths should be type-safe.

---

## Target Architecture

The target architecture should converge toward the following modules:

- `ailib.client`
  - explicit `Client` object
  - shared request/response orchestration
  - timeout and validation orchestration

- `ailib.context`
  - lazy global convenience API
  - `get_client()`, `set_client()`, `set_backend()`, `reset_context()`, `use_backend()`

- `ailib.backends`
  - `Backend` protocol / ABC
  - `StdioBackend`
  - `FileBackend`
  - future experimental transports behind clear stability labels

- `ailib.models`
  - request/response envelopes
  - enums/constants for interaction kinds and status
  - protocol versioning helpers

- `ailib.host`
  - parsing helpers for request markers
  - file readers / response writers
  - convenience helpers for common host outcomes (`ok`, `cancelled`, `error`)

- `ailib.exceptions`
  - narrow, intentional exception hierarchy

- `ailib.validation`
  - JSON-schema validation
  - Pydantic model validation
  - compatibility-safe parsing utilities

- `ailib.logging_utils`
  - structured logging
  - optional redaction hooks
  - stable logger initialization

---

## Release Strategy

Because the repository appears to be in a transitional state, the roadmap should follow a staged release train:

- **0.1.x** — current MVP stabilization and truth alignment
- **0.2.x** — protocolized core without promising full long-term stability yet
- **0.3.x** — validation, host helpers, and packaging maturity
- **0.4.x** — transport hardening and compatibility matrix
- **1.0.0** — stable protocol + stable public API + CI/release/docs completeness
- **1.1+** — ecosystem integrations and advanced transports

If the project later confirms that the “refactor” documented in README/CHANGELOG already exists elsewhere and should be restored, then the numbering can be rebased. Until that is verified, the roadmap should assume the **public repository state** is authoritative.

---

## Milestone 0 — Repository Truth Alignment (Highest Priority)

### Goal
Make code, docs, examples, changelog, packaging metadata, and CI describe the **same product**.

### Deliverables

- Canonical architecture decision record (`docs/adr/001-repository-baseline.md` or similar).
- Version policy decision.
- Inventory of all documented-but-missing or hidden features.
- Alignment pass across:
  - `README.md`
  - `CONTRIBUTING.md`
  - `CHANGELOG.md`
  - `pyproject.toml`
  - package exports
  - examples
  - CI workflow(s)
- “What is stable / experimental / planned” labels in docs.

### Tasks

- Verify the actual source tree and exported API.
- Decide whether the richer documented architecture is:
  - already implemented but not published correctly,
  - partially implemented and needs restoration,
  - aspirational and should be moved into roadmap language.
- Remove or restore drifted references.
- Add a `docs/status.md` page with a precise capability matrix.

### Exit criteria

- A new contributor can clone the repo and understand the real feature set in under 10 minutes.
- `README`, version, examples, and tests all match actual behavior.
- No top-level project document claims features that are absent or untested.

---

## Milestone 1 — Public API Hardening

### Goal
Stabilize the public contract before adding more transports or integrations.

### Deliverables

- Finalized public functions:
  - `ask()`
  - `decide()`
  - `ask_json()`
  - optionally `ask_model()` if model validation lands in the same phase
- Explicit `Client` API.
- Clear timeout handling across all entry points.
- Public exception hierarchy.
- Better defaults for the lazy global context.

### Tasks

- Define canonical function signatures and keyword names.
- Add `timeout_s` consistently across the public API.
- Decide whether `metadata` belongs in 1.0 public contract.
- Guarantee deterministic exception types for:
  - timeout
  - invalid choice
  - invalid JSON
  - protocol mismatch
  - transport failure
  - cancellation
- Replace broad `ValueError` leakage with domain-specific exceptions.
- Add docstrings and typed examples for all public functions.

### Exit criteria

- Public API is documented in one place.
- All public exceptions are listed and tested.
- Semver-breaking changes become easy to identify.

---

## Milestone 2 — Protocol Envelope v2

### Goal
Move from loose payloads to a canonical interruption protocol while keeping pragmatic compatibility.

### Deliverables

- `RequestEnvelope`
- `ResponseEnvelope`
- `request_id`
- `protocol_version`
- `kind`
- `status`
- `error`
- `metadata`
- timestamp fields
- compatibility parser for legacy string/object payloads

### Tasks

- Formalize the interruption schema in code and docs.
- Define major/minor compatibility rules.
- Decide canonical statuses, such as:
  - `ok`
  - `cancelled`
  - `error`
- Define host behavior for unknown versions.
- Preserve a compatibility path for raw string responses in simple `ask()` flows.
- Add a protocol spec document under `docs/protocol.md`.

### Exit criteria

- Every backend speaks the same logical protocol.
- Host helpers and examples are envelope-first.
- Compatibility rules are tested, documented, and versioned.

---

## Milestone 3 — Backend and Transport Hardening

### Goal
Make the MVP backends reliable enough for real orchestrators and long-running automation.

### `StdioBackend` work

- Support response framing with explicit response markers.
- Accept multiline JSON responses safely.
- Support configurable input/output streams for embedding and tests.
- Improve timeout behavior.
- Improve EOF handling and diagnostics.
- Clarify whether request markers go to `stderr`, `stdout`, or are configurable.

### `FileBackend` work

- Atomic writes using temp files + rename.
- Request/response `request_id` matching.
- Stale response detection.
- Cleanup guarantees for success, error, and timeout paths.
- Optional lock files or file-level coordination.
- Better polling diagnostics and backoff options.

### Experimental transport track

Do **not** place these in stable API immediately. Gate them as experimental:

- named pipes / FIFO
- local socket backend
- HTTP loopback backend
- message-bus adapters

### Exit criteria

- Backends are deterministic under repeated tests.
- Concurrency hazards are documented.
- Failure modes produce explicit library exceptions, not silent empties.

---

## Milestone 4 — Validation Layer

### Goal
Make structured outputs safe enough for automation.

### Deliverables

- Optional JSON Schema validation
- Optional Pydantic model validation
- `ask_model()` if accepted into the public API
- schema/model-specific error types
- validation compatibility docs

### Tasks

- Define dependency strategy:
  - minimal core install
  - optional extras (`pydantic`, `schema`, `dev`)
- Decide whether to support only Pydantic v2 or a wider range.
- Add subset validator fallback if full validator is optional.
- Ensure protocol envelopes are not confused with user payloads.
- Add tests for malformed, partial, extra, and legacy payloads.

### Exit criteria

- Structured outputs can be validated locally with predictable failures.
- Schema/model workflows are covered by docs and tests.

---

## Milestone 5 — Testing and Quality Matrix

### Goal
Raise confidence from “works locally” to “safe to embed”.

### Test streams

1. **Unit tests**
   - function behavior
   - exception mapping
   - parser utilities
   - context switching

2. **Backend tests**
   - stdio framing
   - file polling and cleanup
   - timeout paths
   - response mismatch handling

3. **Compatibility tests**
   - legacy raw strings
   - `{\"response\": ...}` payloads
   - envelope version compatibility

4. **Example smoke tests**
   - every example should execute in CI

5. **Cross-platform tests**
   - Linux
   - macOS
   - Windows

6. **Static quality**
   - Ruff or Flake8
   - Black or equivalent formatter
   - MyPy or Pyright for typing

### Tasks

- Consolidate `pytest` and `unittest` strategy.
- Add coverage reporting and a minimum threshold.
- Add property-style tests for parser robustness where helpful.
- Add regression tests for every bug fixed after 0.1.x.

### Exit criteria

- CI is green across supported Python versions.
- Coverage threshold is enforced.
- Examples are no longer documentation-only; they are test assets.

---

## Milestone 6 — Packaging, Build, and Release Discipline

### Goal
Make `ailib` installable, releasable, and trustworthy as a package.

### Deliverables

- Finalized `pyproject.toml`
- build backend decision (stay on setuptools or migrate with intent)
- optional dependency groups
- sdist + wheel validation
- PyPI publish workflow
- signed tags / release notes policy

### Tasks

- Normalize project metadata.
- Ensure version is driven from one source only.
- Add build checks in CI.
- Add release checklist in `docs/releasing.md`.
- Publish first official release once docs, tests, and API truth are aligned.

### Exit criteria

- Fresh environment install works exactly as documented.
- Build artifacts are reproducible and CI-verified.
- Release notes reflect actual changes.

---

## Milestone 7 — Documentation and Developer Experience

### Goal
Make the library easy to adopt by humans and easy to integrate by AI-tool builders.

### Deliverables

- rewritten README around the real stable API
- quickstart for 3 common scenarios:
  - terminal host
  - file-polling host
  - embedded application client
- protocol spec
- troubleshooting guide
- examples index
- migration guide for breaking changes

### Recommended docs structure

- `README.md` — fast entry point
- `docs/architecture.md`
- `docs/protocol.md`
- `docs/backends.md`
- `docs/validation.md`
- `docs/integrations.md`
- `docs/troubleshooting.md`
- `docs/releasing.md`

### Exit criteria

- A new user can complete a roundtrip in under 5 minutes.
- A host-tool author can implement a compatible responder without reading source code.

---

## Milestone 8 — Host Integration Kits

### Goal
Treat the supervising side as first-class product surface.

### Deliverables

- reference host implementation for stdio
- reference host implementation for file mode
- helper utilities for common agent runtimes
- integration notes for Codex/GPT/Gemini/Claude-style supervisors
- optional `ailib-host` CLI for local debugging

### Tasks

- Provide minimal host examples with success, cancellation, and error flows.
- Add protocol transcript fixtures.
- Provide copy-paste examples for tool runners and automation frameworks.
- Design a small CLI to:
  - inspect request files
  - reply manually
  - emit synthetic responses
  - validate envelopes

### Exit criteria

- Host-side adoption no longer requires reverse engineering markers manually.
- Integration examples are executable and tested.

---

## Milestone 9 — Observability, Security, and Governance

### Goal
Prepare the library for usage inside longer-lived and more sensitive automation pipelines.

### Deliverables

- stable logging setup
- optional sensitive-field redaction
- security policy
- deprecation policy
- support matrix for Python versions and backends
- issue templates / PR template / release template

### Tasks

- Define what may appear in logs by default.
- Add metadata redaction hooks.
- Document security assumptions of stdio/file transports.
- Add `SECURITY.md`.
- Add `SUPPORT.md` or equivalent support window docs.
- Introduce ADR process for major compatibility decisions.

### Exit criteria

- Logging is useful without becoming a data leak.
- Compatibility promises are explicit.
- Project governance scales beyond ad-hoc commits.

---

## Milestone 10 — 1.0 Readiness Gate

`ailib` should only declare 1.0 when **all** of the following are true:

- the real source tree matches the public docs;
- the public API is intentionally versioned;
- request/response envelopes are canonical and tested;
- both stable backends are reliable under CI;
- structured validation is available and documented;
- packaging and release flow are reproducible;
- examples are runnable and tested;
- migration/deprecation policy exists;
- the project can explain exactly what is stable, legacy-compatible, and experimental.

---

## Priority Backlog (Suggested Issue Breakdown)

### P0 — Must happen first

1. Align README, changelog, version, and source tree.
2. Add ROADMAP.md and status matrix.
3. Decide canonical version line.
4. Add or restore CI workflow at repository root.
5. Normalize tests and build commands.

### P1 — Core library credibility

6. Add explicit exception hierarchy.
7. Add `Client` and lazy context management.
8. Introduce protocol envelope models.
9. Add `request_id` matching for file backend.
10. Add timeout/error/cancel flow tests.
11. Add response markers and multiline stdio support.
12. Replace silent fallback behavior with explicit errors where appropriate.

### P2 — Structured outputs and packaging

13. Add schema validation.
14. Add model validation.
15. Add optional extras in packaging metadata.
16. Add build validation in CI.
17. Publish first real release artifacts.

### P3 — Adoption and ecosystem

18. Add host helper module and examples.
19. Add debugging CLI.
20. Add integrations guide.
21. Add docs site / richer docs structure.
22. Add cross-platform matrix.

### P4 — Advanced / experimental

23. Socket or HTTP experimental backend.
24. Async facade investigation.
25. Redaction hooks and advanced logging.
26. Protocol transcript tooling.
27. Fuzz/property testing for parsers.

---

## Success Metrics

The roadmap should be considered successful when the project can show measurable improvements such as:

- install success from a fresh environment in < 2 minutes;
- green CI on supported Python versions;
- tested examples for every stable backend;
- stable roundtrip latency under representative local conditions;
- zero ambiguous docs/source mismatches in release branches;
- first external integrations implemented without source-code patching.

---

## Recommended Execution Order

A realistic order of implementation is:

1. repository truth alignment
2. API hardening
3. protocol envelopes
4. backend hardening
5. validation layer
6. CI/build/release discipline
7. docs and examples polish
8. host integration kits
9. governance / security / observability
10. 1.0 release gate

This order prevents the project from building advanced features on top of ambiguous foundations.

---

## Final Direction

The most important strategic decision for `ailib` is not whether it should support more transports or more model helpers first.

The most important decision is this:

> **Should `ailib` remain a tiny, dependable interruption layer with a sharp contract?**

This roadmap assumes the answer is **yes**.

If that stays true, then the project can become extremely valuable precisely because it remains small at the API surface while becoming serious in protocol design, testing, packaging, and host integration.
