# ailib Execution Backlog

This document turns the world-class roadmap into an execution-ready backlog.

It is designed to answer five questions clearly:

1. what should be built first
2. why it matters
3. what each epic contains
4. what counts as done
5. how the work should be sequenced to maximize the chance that `ailib` becomes the default interruption / approval / resume layer

---

## Product Goal

Build `ailib` into the **default control layer for supervised autonomy**.

In practical terms, that means:

- any Python application should be able to emit an interruption request with near-zero friction
- any host or supervisor should be able to inspect, approve, reject, edit, or resume that interruption
- the run should resume durably and deterministically
- the entire lifecycle should be traceable, auditable, and replayable
- integrations with major agent frameworks should feel native

---

## Execution Model

### Work item types

- **Initiative**: a cross-epic program of work
- **Epic**: a large deliverable area that may span multiple releases
- **Issue**: a shippable work item for a single PR or a tightly related PR set
- **Spike**: time-boxed research or prototyping task

### Priority model

- **P0**: mandatory foundation work; blocks multiple epics
- **P1**: strong differentiator; needed for category leadership
- **P2**: important expansion; improves competitiveness and adoption
- **P3**: advanced / future; useful after core leadership is proven

### Status model

- `planned`
- `ready`
- `in_progress`
- `blocked`
- `review`
- `done`
- `deferred`

---

## Release Track

### Release 0 — Truth and Contract
Focus: align repo truth, stabilize public contract, define canonical envelopes

### Release 1 — Durable Resume Core
Focus: checkpoint store API, durable resume, approval objects, transcript logging

### Release 2 — Operational Supervision
Focus: observability, host CLI, replay/fork, policy hooks, richer approvals

### Release 3 — Ecosystem Leadership
Focus: framework adapters, operator UX, external bridges, protocol standardization

### Release 4 — Category Dominance
Focus: compliance, enterprise workflows, side-effect safety contracts, multi-runtime adoption

---

## Initiative A — Become the canonical interruption contract

### Success condition
A developer can look at `ailib` and immediately understand that it is the cleanest, safest, and most portable way to pause and resume supervised execution.

---

## Epic A1 — Repository truth alignment

**Priority:** P0  
**Release target:** Release 0  
**Depends on:** none

### Outcome
Public docs, exports, packaging, changelog, tests, and examples all describe the same real product.

### Issues

#### A1.1 — Audit actual repository capabilities
- Type: issue
- Priority: P0
- Deliverable: one status matrix showing implemented vs documented vs planned
- Acceptance:
  - every exported public symbol is listed
  - every documented feature is marked as implemented, partial, or planned
  - drift is documented in one place

#### A1.2 — Rewrite README around real product state
- Type: issue
- Priority: P0
- Acceptance:
  - README matches actual code behavior
  - stable vs experimental features are labeled
  - install, quickstart, and testing steps are validated

#### A1.3 — Normalize changelog and version strategy
- Type: issue
- Priority: P0
- Acceptance:
  - one canonical version line exists
  - changelog entries reflect actual shipped state
  - release numbering policy is documented

#### A1.4 — Add docs/status.md capability matrix
- Type: issue
- Priority: P0
- Acceptance:
  - matrix covers API, backends, validation, persistence, tracing, integrations, UX
  - each capability has status and owner epic

#### A1.5 — Restore or add CI at repo root
- Type: issue
- Priority: P0
- Acceptance:
  - CI runs tests, build validation, lint, type checks
  - status badge can be added to README

### Definition of done
- a new contributor can understand the real scope in under 10 minutes
- docs no longer claim unimplemented capabilities as shipped

---

## Epic A2 — Public API hardening

**Priority:** P0  
**Release target:** Release 0  
**Depends on:** A1

### Outcome
The public API becomes stable, intentional, and semver-ready.

### Issues

#### A2.1 — Finalize top-level convenience API
- Priority: P0
- Acceptance:
  - `ask`, `decide`, `ask_json` signatures are frozen for 1.0 planning
  - parameter naming is consistent across entry points
  - timeout and metadata behavior are documented

#### A2.2 — Introduce explicit `Client` contract
- Priority: P0
- Acceptance:
  - `Client` is documented as the explicit wiring path
  - convenience functions delegate predictably to `Client`
  - tests cover both global and explicit client usage

#### A2.3 — Replace generic exceptions with domain exceptions
- Priority: P0
- Acceptance:
  - library does not leak broad `ValueError` for protocol/transport failures
  - public exception hierarchy is documented and tested

#### A2.4 — Add API compatibility policy
- Priority: P1
- Acceptance:
  - semver break definition is documented
  - deprecated fields/functions get policy and timeline

### Definition of done
- API is small enough to memorize, but strict enough to trust

---

## Initiative B — Own interruption, approval, and resume semantics

### Success condition
`ailib` becomes the cleanest and most expressive way to represent “execution stopped here, here is what is needed, here is how it resumes.”

---

## Epic B1 — Canonical envelope protocol

**Priority:** P0  
**Release target:** Release 0  
**Depends on:** A2

### Outcome
All transports and integrations speak a single logical protocol.

### Issues

#### B1.1 — Define envelope schema set
- Priority: P0
- Deliverables:
  - `RequestEnvelope`
  - `InterruptionEnvelope`
  - `ResumeEnvelope`
  - `ResponseEnvelope`
- Acceptance:
  - each schema is versioned
  - wire format is documented with examples

#### B1.2 — Define canonical identifiers
- Priority: P0
- Deliverables:
  - `run_id`
  - `thread_id`
  - `request_id`
  - `approval_id`
  - `checkpoint_id`
- Acceptance:
  - all IDs have clear generation and propagation rules
  - transcript and traces include correlation IDs

#### B1.3 — Define action kinds and statuses
- Priority: P0
- Acceptance:
  - kinds cover question, approval, edit, external result, cancel, error
  - statuses cover pending, approved, rejected, edited, cancelled, expired, failed, completed
  - transition rules are documented

#### B1.4 — Add legacy compatibility parser
- Priority: P1
- Acceptance:
  - legacy string/object payloads still work where intended
  - compatibility scope is explicitly bounded and tested

#### B1.5 — Publish protocol spec draft
- Priority: P1
- Acceptance:
  - `docs/protocol.md` includes field-level semantics and examples
  - known non-goals are explicit

### Definition of done
- every stable backend can emit and consume the same logical lifecycle

---

## Epic B2 — Approval object model

**Priority:** P1  
**Release target:** Release 1  
**Depends on:** B1

### Outcome
Approvals become structured, rich, and portable.

### Issues

#### B2.1 — Design approval schema
- Priority: P1
- Acceptance:
  - fields include title, summary, action, risk, diff preview, metadata, deadline, policy tags
  - examples cover shell, code edit, file write, SQL, deployment

#### B2.2 — Add decision types beyond yes/no
- Priority: P1
- Acceptance:
  - approve, reject, edit-and-approve, request-more-context, defer are supported in schema and host helpers

#### B2.3 — Add approval expiration and stale-decision handling
- Priority: P1
- Acceptance:
  - expired approvals fail deterministically
  - resume after expiration produces explicit error/status

#### B2.4 — Add structured edit-and-approve semantics
- Priority: P1
- Acceptance:
  - approver can modify parameters in a typed way
  - resumed run receives edited payload safely

### Definition of done
- an approval is rich enough to be shown in terminal, web UI, or external integrations without ad-hoc translation

---

## Epic B3 — Resume engine

**Priority:** P1  
**Release target:** Release 1  
**Depends on:** B1, B2

### Outcome
Resume becomes a first-class continuation primitive.

### Issues

#### B3.1 — Support resume payload variants
- Priority: P1
- Acceptance:
  - text answer, JSON payload, edited parameters, external result, cancellation reason are supported

#### B3.2 — Add nested interruption support
- Priority: P2
- Acceptance:
  - parent/child interruption relationships are persisted and inspectable

#### B3.3 — Add interruption stack model
- Priority: P2
- Acceptance:
  - stack depth and ancestry can be serialized and restored

#### B3.4 — Add resumable partial-output semantics
- Priority: P2
- Acceptance:
  - partially emitted structured outputs can be resumed or discarded explicitly

### Definition of done
- resume is no longer a loose callback; it is a typed, replayable transition

---

## Initiative C — Make resume durable across crashes, hosts, and time

### Success condition
When a run pauses, it can be resumed later even if the original process has died.

---

## Epic C1 — Checkpoint store abstraction

**Priority:** P0  
**Release target:** Release 1  
**Depends on:** B1

### Outcome
The runtime can persist resumable state through pluggable stores.

### Issues

#### C1.1 — Design checkpoint store interface
- Priority: P0
- Acceptance:
  - create, get, list, update, resume, fork operations are defined
  - schema versioning and metadata fields are included

#### C1.2 — Implement in-memory store
- Priority: P0
- Acceptance:
  - test fixture support exists
  - interface semantics are stable

#### C1.3 — Implement filesystem store
- Priority: P1
- Acceptance:
  - atomic writes are used
  - corruption handling is documented

#### C1.4 — Implement SQLite store
- Priority: P1
- Acceptance:
  - concurrency rules are documented
  - resume works after interpreter restart

#### C1.5 — Implement Postgres store
- Priority: P2
- Acceptance:
  - migrations/versioning strategy exists
  - transactional semantics are documented

### Definition of done
- `ailib` can durably persist and restore paused runs using at least one production-capable store

---

## Epic C2 — Replay, fork, and lineage

**Priority:** P1  
**Release target:** Release 2  
**Depends on:** C1

### Outcome
Operators and developers can study, replay, and branch execution history.

### Issues

#### C2.1 — Add replay from checkpoint
- Priority: P1
- Acceptance:
  - replay can restore a paused run deterministically

#### C2.2 — Add fork-from-checkpoint
- Priority: P1
- Acceptance:
  - a new run can be created from an old checkpoint with new `run_id`

#### C2.3 — Add lineage metadata
- Priority: P1
- Acceptance:
  - parent checkpoint and parent run relationships are stored

#### C2.4 — Add checkpoint lineage graph export
- Priority: P2
- Acceptance:
  - graph can be rendered in JSON or DOT-like form

### Definition of done
- time travel is practical, not conceptual

---

## Epic C3 — Side-effect safety contracts

**Priority:** P1  
**Release target:** Release 2  
**Depends on:** B2, C1

### Outcome
High-risk actions can be approved and resumed with stronger safety guarantees.

### Issues

#### C3.1 — Add pre-commit preview abstraction
- Priority: P1
- Acceptance:
  - approval payload can include preview of proposed side effect

#### C3.2 — Add commit token semantics
- Priority: P2
- Acceptance:
  - approved action can include one-time commit token to prevent accidental duplicate side effects

#### C3.3 — Add rollback metadata fields
- Priority: P2
- Acceptance:
  - rollback hints can be included in approval request and transcript

#### C3.4 — Add idempotency key support
- Priority: P1
- Acceptance:
  - repeated resume does not silently duplicate a protected side effect

### Definition of done
- dangerous actions are safer to supervise and safer to replay

---

## Initiative D — Make the system observable, auditable, and debuggable

### Success condition
Every pause, approval, and resume can be understood after the fact without guessing.

---

## Epic D1 — Event model and tracing

**Priority:** P1  
**Release target:** Release 2  
**Depends on:** B1

### Outcome
Every interruption lifecycle emits structured events and trace spans.

### Issues

#### D1.1 — Define event taxonomy
- Priority: P1
- Acceptance:
  - all core lifecycle events are enumerated and documented

#### D1.2 — Add correlation IDs to logs and events
- Priority: P1
- Acceptance:
  - `run_id`, `thread_id`, `request_id`, `approval_id`, `checkpoint_id` flow through structured logs

#### D1.3 — Add OpenTelemetry-compatible hooks
- Priority: P1
- Acceptance:
  - library can emit lifecycle spans without requiring a specific backend vendor

#### D1.4 — Add pluggable event sink interface
- Priority: P2
- Acceptance:
  - events can be written to stdout, JSONL, OTEL, or custom sink

### Definition of done
- traces tell a complete story of why execution paused and how it resumed

---

## Epic D2 — Transcript capture and audit trail

**Priority:** P1  
**Release target:** Release 1 / 2  
**Depends on:** B1

### Outcome
Every lifecycle can be recorded as a durable transcript.

### Issues

#### D2.1 — Add transcript schema
- Priority: P1
- Acceptance:
  - transcript includes requests, approvals, resumes, checkpoints, errors, timestamps, actor metadata

#### D2.2 — Add JSONL transcript sink
- Priority: P1
- Acceptance:
  - local debugging transcript can be enabled easily

#### D2.3 — Add redaction hooks
- Priority: P1
- Acceptance:
  - caller can redact fields before persistence

#### D2.4 — Add tamper-evident hashing chain
- Priority: P2
- Acceptance:
  - transcript integrity chain can be validated offline

### Definition of done
- a run’s story can be inspected locally and audited later

---

## Initiative E — Win operator experience

### Success condition
Approving a run feels more like reviewing a deployment or PR than debugging transport plumbing.

---

## Epic E1 — Host CLI

**Priority:** P1  
**Release target:** Release 1  
**Depends on:** B1, D2

### Outcome
A supervisor can inspect and resolve interruptions from the terminal.

### Issues

#### E1.1 — Add `ailib-host inspect`
- Priority: P1
- Acceptance:
  - can inspect request/interruption/checkpoint files and render them clearly

#### E1.2 — Add `ailib-host approve`
- Priority: P1
- Acceptance:
  - can approve pending interruption with optional metadata

#### E1.3 — Add `ailib-host reject`
- Priority: P1
- Acceptance:
  - can reject with reason and produce valid resume artifact

#### E1.4 — Add `ailib-host edit`
- Priority: P1
- Acceptance:
  - can edit structured parameters safely before approval

#### E1.5 — Add `ailib-host resume`
- Priority: P1
- Acceptance:
  - can apply a text or JSON continuation to a pending run

### Definition of done
- manual supervision is first-class without needing custom tooling

---

## Epic E2 — Operator TUI and inbox

**Priority:** P2  
**Release target:** Release 3  
**Depends on:** E1, D1, D2

### Outcome
Supervisors get a live inbox of pending work.

### Issues

#### E2.1 — Add TUI pending queue
- Priority: P2
- Acceptance:
  - can list pending approvals with filters by risk, age, run, action type

#### E2.2 — Add approval detail panel
- Priority: P2
- Acceptance:
  - diff/preview, metadata, and lineage are viewable

#### E2.3 — Add stuck interruption view
- Priority: P2
- Acceptance:
  - shows interruptions nearing SLA or expiration

#### E2.4 — Add transcript timeline viewer
- Priority: P2
- Acceptance:
  - events are readable as a chronological lifecycle

### Definition of done
- operator supervision scales beyond one-off CLI commands

---

## Epic E3 — External approval bridges

**Priority:** P2  
**Release target:** Release 3  
**Depends on:** B2, E1

### Outcome
Approvals can happen where operators already work.

### Issues

#### E3.1 — GitHub approval bridge
- Priority: P2
- Acceptance:
  - can map an approval request to GitHub-friendly diff/review flow where applicable

#### E3.2 — Slack approval bridge
- Priority: P2
- Acceptance:
  - can send pending approval summary and capture a secure response path

#### E3.3 — Email / signed-link approval proof of concept
- Priority: P3
- Acceptance:
  - approval decision can be validated securely enough for low-risk workflows

### Definition of done
- operators can approve without living inside raw terminal flows only

---

## Initiative F — Become the substrate every framework can embed

### Success condition
Teams keep their preferred framework but adopt `ailib` for supervision.

---

## Epic F1 — Adapter SDK

**Priority:** P1  
**Release target:** Release 2  
**Depends on:** B1, C1, D1

### Outcome
Third parties can write integrations without patching core internals.

### Issues

#### F1.1 — Add adapter interface for interruption emitters
- Priority: P1
- Acceptance:
  - adapter can convert framework-native pause events into canonical `ailib` envelopes

#### F1.2 — Add adapter interface for resumption consumers
- Priority: P1
- Acceptance:
  - adapter can apply resume payloads back into host/framework runtime

#### F1.3 — Add adapter test harness
- Priority: P1
- Acceptance:
  - adapter authors can run compatibility tests against fixtures

### Definition of done
- integrations become a formal extension surface, not bespoke hacks

---

## Epic F2 — First-party framework adapters

**Priority:** P2  
**Release target:** Release 3  
**Depends on:** F1

### Outcome
`ailib` becomes visible inside the biggest ecosystems.

### Issues

#### F2.1 — LangGraph adapter spike
- Priority: P2
- Acceptance:
  - prototype can wrap interrupt/checkpoint lifecycle into `ailib` schema

#### F2.2 — OpenAI Agents SDK adapter spike
- Priority: P2
- Acceptance:
  - prototype can map sessions and HITL to canonical interruptions

#### F2.3 — PydanticAI adapter spike
- Priority: P2
- Acceptance:
  - prototype can convert deferred tools / approval-required actions into `ailib` approvals

#### F2.4 — AutoGen adapter spike
- Priority: P2
- Acceptance:
  - prototype can emit transcript and state events into `ailib`

#### F2.5 — CrewAI adapter spike
- Priority: P2
- Acceptance:
  - prototype can wrap flow-level interruptions into canonical approvals/resumes

### Definition of done
- at least two external framework integrations are working end-to-end

---

## Initiative G — Policy, compliance, and trust

### Success condition
`ailib` is trusted for high-risk automation, not just toy demos.

---

## Epic G1 — Policy hooks and risk model

**Priority:** P2  
**Release target:** Release 2 / 3  
**Depends on:** B2, C3

### Outcome
Actions can be classified, filtered, and gated by policy.

### Issues

#### G1.1 — Add action risk model
- Priority: P2
- Acceptance:
  - actions can be tagged by risk/severity class

#### G1.2 — Add pre-approval policy hook
- Priority: P2
- Acceptance:
  - policy engine can force human approval, auto-reject, or annotate request

#### G1.3 — Add post-decision policy hook
- Priority: P2
- Acceptance:
  - post-approval execution can still be blocked if policy context changes

#### G1.4 — Add approval-as-code config draft
- Priority: P3
- Acceptance:
  - declarative file format exists for policy rules and approval requirements

### Definition of done
- approval logic can be governed systematically instead of ad hoc

---

## Epic G2 — Security and audit integrity

**Priority:** P2  
**Release target:** Release 3 / 4  
**Depends on:** D2

### Outcome
Audit records become harder to tamper with and easier to trust.

### Issues

#### G2.1 — Add signed approval attestations
- Priority: P2
- Acceptance:
  - approval record can be signed or integrity-tagged

#### G2.2 — Add transcript integrity verification tool
- Priority: P2
- Acceptance:
  - transcript chain can be validated from CLI

#### G2.3 — Add retention and redaction policy docs
- Priority: P2
- Acceptance:
  - users know how to minimize sensitive persistence risk

### Definition of done
- audit trail is stronger than plain append-only logging

---

## Initiative H — Standardize the category

### Success condition
`ailib` is not just a library; it becomes a protocol and reference implementation.

---

## Epic H1 — Universal interruption record

**Priority:** P3  
**Release target:** Release 4  
**Depends on:** B1, F1

### Outcome
A stable format emerges that non-`ailib` systems can emit and consume.

### Issues

#### H1.1 — Publish language-neutral protocol draft
- Priority: P3
- Acceptance:
  - wire format avoids Python-only assumptions

#### H1.2 — Add protocol conformance fixtures
- Priority: P3
- Acceptance:
  - external runtimes can validate against shared fixtures

#### H1.3 — Add compatibility test suite docs
- Priority: P3
- Acceptance:
  - third-party implementers know how to self-certify compatibility

### Definition of done
- the protocol can outlive the Python package if needed

---

## Epic H2 — Category thought leadership assets

**Priority:** P3  
**Release target:** Release 4  
**Depends on:** H1

### Outcome
The project makes a credible case for becoming the standard.

### Issues

#### H2.1 — Write reference architecture paper
- Priority: P3
- Acceptance:
  - explains why interruption / approval / resume deserves a standalone layer

#### H2.2 — Publish competitive comparison doc
- Priority: P3
- Acceptance:
  - comparison is honest, specific, and focused on category fit

#### H2.3 — Publish integration blueprints
- Priority: P3
- Acceptance:
  - examples show how to embed `ailib` under multiple frameworks

### Definition of done
- adoption argument is strong enough for external teams to standardize on it

---

## Sequencing Rules

### Build in this order

1. A1 Repository truth alignment
2. A2 Public API hardening
3. B1 Canonical envelope protocol
4. C1 Checkpoint store abstraction
5. B2 Approval object model
6. B3 Resume engine
7. D2 Transcript capture
8. E1 Host CLI
9. D1 Event model and tracing
10. C2 Replay, fork, lineage
11. C3 Side-effect safety contracts
12. F1 Adapter SDK
13. G1 Policy hooks and risk model
14. E2 Operator TUI and inbox
15. F2 First-party framework adapters
16. E3 External approval bridges
17. G2 Security and audit integrity
18. H1 Universal interruption record
19. H2 Category thought leadership assets

### Why this order wins

- first, make the contract trustworthy
- then, make it durable
- then, make it pleasant to operate
- then, make it observable and safe
- then, make it easy for other ecosystems to adopt
- finally, push toward standardization

---

## First 12 Issues to Actually Open

If only a small number of issues are opened immediately, open these first:

1. Audit actual repository capabilities
2. Rewrite README around real product state
3. Restore or add CI at repo root
4. Finalize top-level convenience API
5. Introduce explicit `Client` contract
6. Define envelope schema set
7. Define canonical identifiers
8. Define action kinds and statuses
9. Design checkpoint store interface
10. Design approval schema
11. Add transcript schema
12. Add `ailib-host inspect`

This set is enough to move from idea-stage ambition into real execution.

---

## Definition of Ready for Any Issue

An issue is ready when:

- problem statement is explicit
- scope boundary is clear
- acceptance criteria are testable
- dependencies are known
- target release is assigned
- examples or fixtures are identified where needed

## Definition of Done for Any Issue

An issue is done when:

- implementation exists
- tests cover success and failure cases
- docs are updated
- changelog/release note impact is considered
- behavior is reproducible from a clean environment
- any new protocol or schema changes include fixtures/examples

---

## Leadership Checkpoints

At the end of each release, ask these questions:

### After Release 0
- is the repo finally honest and coherent?
- is the protocol direction unmistakable?

### After Release 1
- can paused runs survive process death?
- are approvals and resumes genuinely structured?

### After Release 2
- can operators inspect, trace, replay, and safely supervise runs?

### After Release 3
- can other frameworks adopt `ailib` without painful glue code?

### After Release 4
- is `ailib` now the obvious reference implementation for the category?

---

## Final Standard

This backlog should be considered successful only when `ailib` is strong enough that the following statement feels realistic rather than aspirational:

> If an autonomous system needs to pause, ask, wait, resume, explain itself, and produce an audit trail, the safest default choice is `ailib`.
