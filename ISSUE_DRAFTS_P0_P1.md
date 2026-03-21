# ailib Issue Drafts — P0 / P1

This file contains ready-to-open GitHub issue drafts derived from the roadmap and execution backlog.

How to use:

- create one GitHub issue per section below
- keep titles as-is unless repo naming conventions change
- use the suggested labels if/when labels are added to the repository
- preserve dependencies and acceptance criteria

Suggested base labels:

- `priority:P0`
- `priority:P1`
- `type:docs`
- `type:api`
- `type:protocol`
- `type:persistence`
- `type:observability`
- `type:cli`
- `type:testing`
- `type:release`

---

## 1) Audit actual repository capabilities

**Suggested labels:** `priority:P0`, `type:docs`  
**Depends on:** none

### Summary
Create a single source of truth for what `ailib` actually implements today versus what is only documented or planned.

### Why
The repository currently appears to be in a transitional state. Before building toward world-class interruption / approval / resume, the project needs one honest capability baseline.

### Scope
- inventory exported API surface
- inventory actual modules and stable entry points
- compare code vs README vs CONTRIBUTING vs CHANGELOG vs examples
- classify each capability as:
  - implemented
  - partial
  - planned
  - drifted / inaccurate

### Deliverables
- `docs/status.md` or equivalent capability matrix
- concise drift summary
- recommended corrective actions

### Acceptance criteria
- every public symbol is accounted for
- every documented feature is tagged by real status
- major drift areas are explicit
- the output is good enough to guide README/version cleanup

### Definition of done
- a contributor can inspect one document and understand current project truth

---

## 2) Rewrite README around real product state

**Suggested labels:** `priority:P0`, `type:docs`  
**Depends on:** Issue 1

### Summary
Rewrite `README.md` so it matches the actual state of the codebase and clearly distinguishes shipped, experimental, and planned functionality.

### Why
The README is the public face of the project. If it overstates or mismatches the code, trust drops immediately.

### Scope
- validate install steps
- validate quickstart
- validate examples
- label stable vs experimental features
- align terminology around interruption / approval / resume

### Deliverables
- updated README
- stable/experimental notes
- validated quickstart examples

### Acceptance criteria
- setup works from a clean environment
- documented commands run as written
- terminology is consistent with roadmap/backlog
- no absent feature is described as shipped

### Definition of done
- README is truthful, concise, and onboarding-friendly

---

## 3) Restore or add CI at repository root

**Suggested labels:** `priority:P0`, `type:testing`, `type:release`  
**Depends on:** none

### Summary
Ensure the repository has a working root-level CI workflow that validates tests, build, lint, and typing.

### Why
The project cannot credibly become the default control layer for supervised autonomy without reliable automated validation.

### Scope
- test suite execution
- build validation
- lint
- typing
- supported Python version matrix

### Deliverables
- `.github/workflows/ci.yml`
- passing CI on main
- optional badge-ready output

### Acceptance criteria
- CI runs on pushes and PRs
- CI validates package build
- CI fails on test/lint/type errors
- documented local commands match CI steps

### Definition of done
- CI is green on the default branch with no manual steps required

---

## 4) Finalize top-level convenience API

**Suggested labels:** `priority:P0`, `type:api`  
**Depends on:** Issue 1

### Summary
Freeze and document the intended top-level convenience API for `ask`, `decide`, and `ask_json`.

### Why
A small, stable API surface is a core advantage over heavier frameworks.

### Scope
- finalize function signatures
- normalize parameter names
- define timeout semantics
- define metadata semantics
- define exception behavior

### Deliverables
- documented signature contract
- tests covering public entry points
- migration note if needed

### Acceptance criteria
- all convenience functions behave consistently
- timeout handling is documented and tested
- metadata behavior is explicit
- semver-sensitive API decisions are recorded

### Definition of done
- public convenience API is stable enough to plan 1.0 around it

---

## 5) Introduce explicit `Client` contract

**Suggested labels:** `priority:P0`, `type:api`  
**Depends on:** Issue 4

### Summary
Define and document `Client` as the explicit wiring path for applications that do not want global convenience state.

### Why
The library needs a rigorous core abstraction beneath the convenience layer.

### Scope
- define responsibilities of `Client`
- define relationship between `Client` and global helpers
- document explicit usage patterns
- add tests for direct `Client` usage

### Deliverables
- stable `Client` contract
- docs and examples
- tests

### Acceptance criteria
- `Client` behavior is documented and tested
- convenience API delegates predictably to `Client`
- explicit and implicit usage paths are both supported intentionally

### Definition of done
- applications can use `ailib` without relying on implicit globals

---

## 6) Define envelope schema set

**Suggested labels:** `priority:P0`, `type:protocol`  
**Depends on:** Issue 4, Issue 5

### Summary
Define the canonical schema set for request, interruption, resume, and response lifecycles.

### Why
World-class interruption / approval / resume starts with a strong protocol contract.

### Scope
- `RequestEnvelope`
- `InterruptionEnvelope`
- `ResumeEnvelope`
- `ResponseEnvelope`
- schema versioning strategy
- example wire payloads

### Deliverables
- schema definitions in code
- `docs/protocol.md` draft
- fixtures/examples

### Acceptance criteria
- all core lifecycles map onto one envelope family
- fields are named consistently
- sample payloads exist for all major flows
- schema versioning rules are documented

### Definition of done
- the project has one canonical protocol direction

---

## 7) Define canonical identifiers

**Suggested labels:** `priority:P0`, `type:protocol`  
**Depends on:** Issue 6

### Summary
Define the ID model for correlating runs, threads, requests, approvals, and checkpoints.

### Why
Durability, replay, tracing, and auditability all depend on a clean ID strategy.

### Scope
- `run_id`
- `thread_id`
- `request_id`
- `approval_id`
- `checkpoint_id`
- generation rules
- propagation rules

### Deliverables
- identifier definitions
- docs/examples
- correlation tests

### Acceptance criteria
- each ID has clear lifecycle semantics
- logs/transcripts can correlate on IDs
- IDs are not ambiguous across resume/replay paths

### Definition of done
- correlation model is stable enough for tracing and persistence work

---

## 8) Define action kinds and statuses

**Suggested labels:** `priority:P0`, `type:protocol`  
**Depends on:** Issue 6

### Summary
Define the canonical action kinds and lifecycle statuses for interruption and approval flows.

### Why
Without explicit kinds and statuses, approvals and resumes stay underspecified.

### Scope
- kinds such as:
  - question
  - approval
  - edit_request
  - provide_input
  - external_result
  - cancel
  - error
- statuses such as:
  - pending
  - approved
  - rejected
  - edited
  - cancelled
  - expired
  - failed
  - completed
- transition rules

### Deliverables
- enums/constants/models
- transition documentation
- protocol fixtures

### Acceptance criteria
- kinds and statuses cover core use cases
- illegal transitions are documented or prevented
- host-side semantics are clear

### Definition of done
- lifecycle language is explicit across code, docs, and tests

---

## 9) Design checkpoint store interface

**Suggested labels:** `priority:P0`, `type:persistence`  
**Depends on:** Issue 6, Issue 7

### Summary
Design the pluggable interface for saving and restoring paused execution state.

### Why
Durable resume is one of the strongest ways to leap ahead of simpler libraries and approach category leadership.

### Scope
- create checkpoint
- get checkpoint
- list checkpoints
- resume checkpoint
- fork checkpoint
- metadata/versioning

### Deliverables
- checkpoint store interface
- in-memory reference implementation design or stub
- usage examples

### Acceptance criteria
- interface supports at least memory, filesystem, SQLite, and Postgres implementations in future
- checkpoint metadata includes enough information for resume and replay
- API is transport-agnostic

### Definition of done
- persistence work can begin without rethinking the contract

---

## 10) Design approval schema

**Suggested labels:** `priority:P0`, `type:protocol`  
**Depends on:** Issue 6, Issue 8

### Summary
Design the structured approval object used across all high-risk or human-gated actions.

### Why
This is a core differentiator. `ailib` should support approvals richer than yes/no.

### Scope
- title
- summary
- risk level
- proposed action
- diff/preview
- structured parameters
- policy tags
- approver metadata
- expiration/deadline
- decision types beyond simple approve/reject

### Deliverables
- approval schema draft
- examples for shell/code/file/SQL/deploy cases
- typed decision model

### Acceptance criteria
- approvals are portable across terminal, UI, and external integrations
- edit-and-approve is representable
- expiration and stale decisions are representable

### Definition of done
- approval becomes a first-class portable object

---

## 11) Add transcript schema

**Suggested labels:** `priority:P1`, `type:observability`  
**Depends on:** Issue 6, Issue 7

### Summary
Define the transcript format used to record interruption, approval, resume, checkpoint, and error lifecycles.

### Why
Auditability and replay start with a good transcript model.

### Scope
- transcript event schema
- correlation IDs
- actor metadata
- timestamps
- status transitions
- error representation
- redaction hooks design notes

### Deliverables
- transcript schema
- JSONL example sink design
- example transcript fixture

### Acceptance criteria
- transcript can reconstruct the lifecycle of a run
- transcript includes enough correlation to support replay/debugging later
- transcript format is append-friendly and tooling-friendly

### Definition of done
- there is one clear audit trail model for local and future remote use

---

## 12) Add `ailib-host inspect`

**Suggested labels:** `priority:P1`, `type:cli`  
**Depends on:** Issue 6, Issue 10, Issue 11

### Summary
Add the first host CLI command to inspect pending interruptions, requests, or checkpoints clearly from the terminal.

### Why
A strong operator experience is critical if `ailib` is going to become the default supervision substrate.

### Scope
- inspect request file or interruption artifact
- render rich human-readable view
- show IDs, status, kind, summary, risk, metadata, and relevant payloads
- support raw JSON output mode

### Deliverables
- `ailib-host inspect`
- docs/examples
- sample artifacts for testing

### Acceptance criteria
- command can inspect at least one canonical artifact format
- output is clear enough to support manual supervision
- raw mode supports automation/debugging

### Definition of done
- `ailib` has the first operator-facing tool in place

---

## 13) Add legacy compatibility parser

**Suggested labels:** `priority:P1`, `type:protocol`  
**Depends on:** Issue 6, Issue 8

### Summary
Add a clearly bounded compatibility parser for legacy raw-string and legacy-object workflows.

### Why
Compatibility can smooth adoption, but it must be explicit and controlled.

### Scope
- raw string compatibility where intended
- legacy object compatibility where intended
- disambiguation rules
- bounded scope documentation

### Deliverables
- parser implementation
- tests for success and failure paths
- compatibility notes in docs

### Acceptance criteria
- compatibility behavior is deterministic
- parser does not silently reinterpret canonical payloads incorrectly
- unsupported legacy shapes fail clearly

### Definition of done
- compatibility is intentional instead of accidental

---

## 14) Add OpenTelemetry-compatible event hooks

**Suggested labels:** `priority:P1`, `type:observability`  
**Depends on:** Issue 7, Issue 11

### Summary
Expose lifecycle hooks that can feed OpenTelemetry-compatible tracing without binding the library to a specific vendor.

### Why
Strong observability is one of the main category benchmarks set by larger frameworks.

### Scope
- lifecycle event taxonomy
- hook interface
- span-friendly metadata
- correlation ID propagation

### Deliverables
- event hook API
- example sink/exporter
- docs

### Acceptance criteria
- interruption/approval/resume lifecycles emit structured events
- events include correlation IDs
- hooks can be no-op by default

### Definition of done
- `ailib` has a credible path to production-grade tracing

---

## 15) Add transcript logger

**Suggested labels:** `priority:P1`, `type:observability`  
**Depends on:** Issue 11

### Summary
Implement a transcript logger that writes lifecycle events to an append-friendly local format, such as JSONL.

### Why
This is the simplest practical path to debuggability, auditability, and future replay.

### Scope
- local transcript sink
- file rotation/basic safety notes
- correlation IDs
- event serialization
- optional redaction hooks

### Deliverables
- transcript logger implementation
- examples
- tests

### Acceptance criteria
- a real run can generate a readable transcript
- transcript contains enough data to inspect what paused and why
- logger can be enabled without invasive wiring

### Definition of done
- local transcript capture is real, not just planned

---

## 16) Add CLI commands for approve / reject / resume

**Suggested labels:** `priority:P1`, `type:cli`  
**Depends on:** Issue 10, Issue 12

### Summary
Add the next host CLI commands that allow supervisors to resolve interruptions from the terminal.

### Why
Inspect without action is only half the operator story.

### Scope
- `ailib-host approve`
- `ailib-host reject`
- `ailib-host resume`
- optional structured edit support later

### Deliverables
- CLI commands
- docs/examples
- fixtures/tests

### Acceptance criteria
- host can approve, reject, or resume using canonical artifacts
- resulting artifacts are protocol-valid
- failure/error flows are handled clearly

### Definition of done
- terminal-based supervision becomes end-to-end usable

---

## Suggested opening order

Open in this order:

1. Audit actual repository capabilities
2. Rewrite README around real product state
3. Restore or add CI at repository root
4. Finalize top-level convenience API
5. Introduce explicit `Client` contract
6. Define envelope schema set
7. Define canonical identifiers
8. Define action kinds and statuses
9. Design checkpoint store interface
10. Design approval schema
11. Add transcript schema
12. Add `ailib-host inspect`
13. Add legacy compatibility parser
14. Add OpenTelemetry-compatible event hooks
15. Add transcript logger
16. Add CLI commands for approve / reject / resume
