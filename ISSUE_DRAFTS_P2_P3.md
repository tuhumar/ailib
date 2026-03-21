# ailib Issue Drafts — P2 / P3

This file contains ready-to-open GitHub issue drafts for the remaining roadmap after the P0/P1 foundation set.

How to use:

- create one GitHub issue per section below
- keep titles as-is unless repo naming conventions change
- use the suggested labels if/when labels are added to the repository
- preserve dependencies and acceptance criteria
- open these after or alongside the foundational issues from `ISSUE_DRAFTS_P0_P1.md`

Suggested base labels:

- `priority:P2`
- `priority:P3`
- `type:protocol`
- `type:persistence`
- `type:observability`
- `type:cli`
- `type:integrations`
- `type:policy`
- `type:security`
- `type:ux`
- `type:standards`

---

## 1) Implement in-memory checkpoint store

**Suggested labels:** `priority:P2`, `type:persistence`  
**Depends on:** P0 Issue 9

### Summary
Implement the first reference checkpoint store using in-memory persistence for tests, examples, and contract validation.

### Why
The project needs one minimal concrete store to validate checkpoint semantics before moving into filesystem, SQLite, or Postgres backends.

### Scope
- create/get/list/update checkpoint operations
- resume/fork placeholders if supported by the interface
- test fixture integration
- clear lifecycle semantics

### Deliverables
- in-memory checkpoint store implementation
- tests
- example usage

### Acceptance criteria
- store passes the checkpoint interface contract tests
- paused state can be retrieved and resumed in-process
- store behavior is deterministic under tests

### Definition of done
- persistence contract is proven against one concrete implementation

---

## 2) Implement filesystem checkpoint store

**Suggested labels:** `priority:P2`, `type:persistence`  
**Depends on:** P2 Issue 1

### Summary
Add a filesystem-backed checkpoint store for simple local durability and operator-friendly debugging.

### Why
A file-based durable store is the easiest path to cross-process resume in local environments.

### Scope
- atomic writes
- safe overwrite/update semantics
- corruption detection strategy
- checkpoint metadata storage
- local inspection friendliness

### Deliverables
- filesystem checkpoint store
- tests for restart and recovery scenarios
- usage docs

### Acceptance criteria
- paused state survives process restart
- writes are atomic enough to avoid common corruption cases
- stale/corrupt state handling is explicit

### Definition of done
- local durable resume works without a database

---

## 3) Implement SQLite checkpoint store

**Suggested labels:** `priority:P2`, `type:persistence`  
**Depends on:** P2 Issue 1

### Summary
Implement a SQLite-backed checkpoint store as the first production-leaning durable persistence backend.

### Why
SQLite is a strong middle ground between local simplicity and real durability.

### Scope
- schema creation/versioning
- create/get/list/update checkpoint operations
- restart-safe resume
- concurrency notes and lock behavior

### Deliverables
- SQLite store
- schema/migration note
- tests

### Acceptance criteria
- checkpoints survive interpreter restarts
- store supports realistic local workflows
- schema versioning strategy is documented

### Definition of done
- `ailib` has one production-capable durable store suitable for many users

---

## 4) Implement Postgres checkpoint store

**Suggested labels:** `priority:P2`, `type:persistence`  
**Depends on:** P2 Issue 3

### Summary
Add a Postgres-backed checkpoint store for multi-process and service-oriented deployments.

### Why
If `ailib` is to become the default substrate for supervised autonomy, it needs a database backend suitable for team and service environments.

### Scope
- relational schema
- transactional checkpoint writes
- migration/versioning strategy
- resume/fork support
- operational notes

### Deliverables
- Postgres store
- migrations/schema docs
- integration tests

### Acceptance criteria
- checkpoints can be created/restored transactionally
- concurrency assumptions are documented
- store works in CI or containerized integration tests

### Definition of done
- team-scale durable resume is supported by a real database backend

---

## 5) Add replay from checkpoint

**Suggested labels:** `priority:P2`, `type:persistence`, `type:observability`  
**Depends on:** P2 Issue 2 or 3

### Summary
Allow a paused or completed run to be replayed from a stored checkpoint.

### Why
Replay is one of the most powerful differentiators against simpler libraries.

### Scope
- restore checkpoint into replay mode
- deterministic replay semantics where possible
- operator/developer-facing API or CLI entry point
- replay transcript markers

### Deliverables
- replay primitive/API
- tests
- docs/examples

### Acceptance criteria
- checkpoint can be replayed intentionally
- replay lifecycle is distinguishable from live resume
- docs describe limits of determinism clearly

### Definition of done
- replay is a real debugging and audit tool, not a concept

---

## 6) Add fork-from-checkpoint support

**Suggested labels:** `priority:P2`, `type:persistence`  
**Depends on:** P2 Issue 5

### Summary
Support creating a new run lineage from an existing checkpoint.

### Why
Forking unlocks experimentation, time-travel debugging, and alternate approval paths.

### Scope
- fork API
- new `run_id` allocation
- parent-child lineage tracking
- transcript/metadata annotations

### Deliverables
- fork primitive/API
- tests
- lineage docs

### Acceptance criteria
- a new run can be created from an old checkpoint without mutating the original lineage
- lineage metadata is persisted

### Definition of done
- alternate futures can be explored safely

---

## 7) Add checkpoint lineage graph export

**Suggested labels:** `priority:P2`, `type:persistence`, `type:ux`  
**Depends on:** P2 Issue 6

### Summary
Export checkpoint and run lineage in a machine-readable graph form.

### Why
Lineage becomes more useful when it can be visualized or inspected externally.

### Scope
- JSON export shape
- optional DOT-like export
- parent/child relationships
- operator docs

### Deliverables
- export API or CLI
- fixtures/examples
- docs

### Acceptance criteria
- lineage can be exported for a non-trivial fork/replay history
- schema is documented and stable enough for tooling

### Definition of done
- lineage is accessible to future UIs and external tools

---

## 8) Add nested interruption support

**Suggested labels:** `priority:P2`, `type:protocol`  
**Depends on:** P0 Issue 6, P0 Issue 7, P0 Issue 8

### Summary
Support interruptions that occur inside other interruption-driven workflows.

### Why
Complex supervised systems often need nested pauses and sub-decisions.

### Scope
- parent interruption references
- nested status rules
- transcript semantics
- serialization rules

### Deliverables
- nested interruption model
- tests
- docs/examples

### Acceptance criteria
- nested interruption relationships are persisted and inspectable
- parent/child semantics are explicit
- resume behavior remains deterministic

### Definition of done
- `ailib` can model multi-layer supervision cleanly

---

## 9) Add interruption stack model

**Suggested labels:** `priority:P2`, `type:protocol`  
**Depends on:** P2 Issue 8

### Summary
Represent interruption ancestry and stack depth explicitly.

### Why
Nested interruption alone is not enough; operators and tooling need stack context.

### Scope
- stack/ancestry fields
- serialization rules
- restoration semantics
- stack inspection helpers

### Deliverables
- interruption stack model
- docs
- tests

### Acceptance criteria
- stack ancestry can be reconstructed from canonical artifacts
- stack depth is explicit and testable

### Definition of done
- interruption context becomes richer for tooling and audits

---

## 10) Add resumable partial-output semantics

**Suggested labels:** `priority:P2`, `type:protocol`  
**Depends on:** P0 Issue 6, P0 Issue 10

### Summary
Allow partial structured outputs or partially completed actions to be resumed or discarded intentionally.

### Why
Long-running or streaming tasks may stop mid-result; resumption should handle that explicitly.

### Scope
- partial-output markers
- partial resume payloads
- discard/finalize semantics
- docs and examples

### Deliverables
- protocol support
- tests
- examples

### Acceptance criteria
- partial output state is representable
- resume/discard behavior is explicit and validated

### Definition of done
- interrupted structured work is not forced into all-or-nothing flows only

---

## 11) Add pre-commit preview abstraction

**Suggested labels:** `priority:P2`, `type:protocol`, `type:policy`  
**Depends on:** P0 Issue 10

### Summary
Add a standard way to attach previews or diffs of proposed side effects before approval.

### Why
Safer approvals require seeing what will happen before committing the change.

### Scope
- preview object model
- diff/plan attachment fields
- support for code/file/shell/SQL/infrastructure previews

### Deliverables
- preview abstraction
- examples
- docs

### Acceptance criteria
- approval payloads can include pre-commit previews consistently
- previews are structured enough for future UIs to render

### Definition of done
- approval is based on a visible proposed change, not blind trust

---

## 12) Add idempotency key support for protected side effects

**Suggested labels:** `priority:P2`, `type:protocol`, `type:security`  
**Depends on:** P2 Issue 11

### Summary
Add idempotency support so retried or duplicated resume flows do not silently repeat protected side effects.

### Why
Resume safety is critical when approvals can trigger real-world actions.

### Scope
- idempotency key fields
- retry semantics
- docs/examples
- validation rules

### Deliverables
- protocol field support
- helper utilities
- tests

### Acceptance criteria
- duplicate execution attempts can be identified and handled intentionally
- docs explain guarantee boundaries clearly

### Definition of done
- resumption is safer for high-risk operations

---

## 13) Add lifecycle event taxonomy

**Suggested labels:** `priority:P2`, `type:observability`  
**Depends on:** P0 Issue 11, P0 Issue 14

### Summary
Define the full event taxonomy for interruption, approval, resume, checkpoint, and run lifecycle events.

### Why
A clean event model is the basis for tracing, transcripts, analytics, and future UIs.

### Scope
- event names
- required fields
- optional fields
- correlation requirements
- event ordering guidance

### Deliverables
- event taxonomy spec
- examples
- docs

### Acceptance criteria
- all core lifecycle phases are covered
- events can be consumed by transcript sinks and OTEL hooks consistently

### Definition of done
- the project has a durable observability vocabulary

---

## 14) Add pluggable event sink interface

**Suggested labels:** `priority:P2`, `type:observability`  
**Depends on:** P2 Issue 13

### Summary
Allow lifecycle events to be emitted to multiple sinks such as JSONL, stdout, OTEL, or custom handlers.

### Why
Different deployments need different observability backends.

### Scope
- sink interface
- default sink behavior
- sink registration/configuration
- example sink implementations

### Deliverables
- sink interface
- tests
- docs/examples

### Acceptance criteria
- event emission is backend-neutral
- multiple sink strategies can be supported without invasive changes

### Definition of done
- observability becomes extensible rather than hard-coded

---

## 15) Add transcript redaction hooks

**Suggested labels:** `priority:P2`, `type:observability`, `type:security`  
**Depends on:** P0 Issue 15

### Summary
Allow callers to redact sensitive fields before transcript persistence or event emission.

### Why
Auditability should not come at the cost of unnecessary sensitive data leakage.

### Scope
- redaction hook API
- field/path-based redaction patterns
- docs and examples
- tests

### Deliverables
- redaction hooks
- examples
- docs

### Acceptance criteria
- users can suppress or mask selected fields consistently
- hooks work with transcript and event sinks

### Definition of done
- observability has a privacy-aware escape hatch

---

## 16) Add `ailib-host edit` for structured edit-and-approve flows

**Suggested labels:** `priority:P2`, `type:cli`  
**Depends on:** P0 Issue 16

### Summary
Add a host CLI command that allows structured parameter editing before approval.

### Why
Edit-and-approve is one of the clearest ways for `ailib` to outperform simplistic yes/no approval flows.

### Scope
- structured parameter editing path
- validation before writing updated approval/resume artifacts
- raw JSON edit mode if needed

### Deliverables
- `ailib-host edit`
- docs
- fixtures/tests

### Acceptance criteria
- edited approval payloads are validated before acceptance
- command is usable for at least one structured approval scenario

### Definition of done
- CLI supervision supports meaningful operator intervention

---

## 17) Add operator TUI pending queue

**Suggested labels:** `priority:P2`, `type:ux`, `type:cli`  
**Depends on:** P0 Issue 12, P0 Issue 16, P2 Issue 13

### Summary
Create a terminal UI showing pending interruptions and approvals in a queue/inbox format.

### Why
If `ailib` becomes popular, operators will need a scalable supervision surface beyond one-off commands.

### Scope
- pending item list
- filters by risk, age, status, action type
- selection/detail view
- basic navigation/actions

### Deliverables
- TUI inbox prototype
- screenshots/docs
- tests where practical

### Acceptance criteria
- TUI can list and inspect multiple pending items
- operators can triage work from one screen

### Definition of done
- supervision begins to feel productized

---

## 18) Add transcript timeline viewer

**Suggested labels:** `priority:P2`, `type:ux`, `type:observability`  
**Depends on:** P0 Issue 15, P2 Issue 17

### Summary
Add a timeline-oriented transcript viewer for operators and developers.

### Why
Chronological viewing is one of the most intuitive ways to understand interrupted execution.

### Scope
- chronological event view
- key metadata surfaces
- filtering/search basics
- CLI/TUI-first implementation

### Deliverables
- timeline viewer
- docs/examples

### Acceptance criteria
- a non-trivial run transcript can be inspected in chronological form clearly
- timeline can highlight approvals, resumes, errors, and checkpoints

### Definition of done
- audit and debugging become materially easier

---

## 19) Add GitHub approval bridge

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P0 Issue 10, P2 Issue 11

### Summary
Prototype a GitHub-oriented approval bridge for code-agent or file-change approvals.

### Why
GitHub is one of the most natural places to meet developers where they already review changes.

### Scope
- map approval preview/diff into GitHub-friendly shape
- link approval decision back into canonical `ailib` artifacts
- document trust boundaries

### Deliverables
- integration prototype or adapter
- docs
- example flow

### Acceptance criteria
- at least one code/file approval flow can be represented through a GitHub-oriented bridge
- `ailib` remains the source of truth for protocol state

### Definition of done
- GitHub becomes a viable operator surface for some approvals

---

## 20) Add Slack approval bridge

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P0 Issue 10, P0 Issue 16

### Summary
Prototype a Slack bridge for lightweight operator approvals.

### Why
Many real teams supervise workflows from chat first.

### Scope
- summary notification payload
- secure response path back to `ailib`
- docs around trust/risk limitations

### Deliverables
- Slack bridge prototype
- docs
- example flow

### Acceptance criteria
- approval can be surfaced and resolved from Slack in at least one supported path
- canonical protocol artifacts remain authoritative

### Definition of done
- chat-based supervision is viable for lower-friction workflows

---

## 21) Add adapter interface for interruption emitters and resumption consumers

**Suggested labels:** `priority:P2`, `type:integrations`, `type:api`  
**Depends on:** P0 Issue 6, P0 Issue 7, P2 Issue 14

### Summary
Create a formal adapter interface so external frameworks can emit canonical interruptions and consume resumes without patching core internals.

### Why
`ailib` wins by becoming the substrate other ecosystems can embed.

### Scope
- interruption emitter interface
- resume consumer interface
- adapter lifecycle docs
- compatibility expectations

### Deliverables
- adapter interface definitions
- docs/examples
- tests or harness stubs

### Acceptance criteria
- adapter authors have one formal extension surface
- framework integrations do not require unstable private APIs

### Definition of done
- interoperability is intentional and scalable

---

## 22) Add adapter compatibility test harness

**Suggested labels:** `priority:P2`, `type:integrations`, `type:testing`  
**Depends on:** P2 Issue 21

### Summary
Provide a harness that lets adapter authors verify conformance against canonical fixtures and lifecycle expectations.

### Why
Adapters need a shared correctness bar if `ailib` is to become a standard layer.

### Scope
- fixture suite
- protocol conformance tests
- adapter author docs

### Deliverables
- test harness
- fixtures
- docs

### Acceptance criteria
- an adapter can be validated against reusable compatibility tests
- harness covers success and failure cases

### Definition of done
- integrations can be built with confidence and consistency

---

## 23) Add LangGraph adapter spike

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P2 Issue 21, P2 Issue 22

### Summary
Prototype mapping LangGraph interrupt/checkpoint flows into canonical `ailib` artifacts.

### Why
LangGraph is one of the strongest adjacent products in the category and a key interoperability target. citeturn709000search0turn709000search2

### Scope
- map pause/interruption semantics
- map durable state/checkpoint concepts
- identify impedance mismatches

### Deliverables
- prototype adapter or design spike doc
- findings and recommended next steps

### Acceptance criteria
- at least one realistic interruption flow is demonstrated or fully designed
- compatibility gaps are documented honestly

### Definition of done
- `ailib` has a concrete adoption path for LangGraph users

---

## 24) Add OpenAI Agents SDK adapter spike

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P2 Issue 21, P2 Issue 22

### Summary
Prototype mapping session/HITL/resume semantics from OpenAI Agents SDK into canonical `ailib` artifacts.

### Why
OpenAI’s SDK is a major reference point for modern agent ergonomics and observability. citeturn884581search0turn884581search2

### Scope
- map session continuity
- map HITL/interruption/resume concepts
- identify trace/metadata alignment opportunities

### Deliverables
- prototype or spike document
- compatibility notes

### Acceptance criteria
- at least one realistic approval/resume flow is mapped
- adapter boundaries are documented

### Definition of done
- there is a practical bridge story for OpenAI Agents SDK users

---

## 25) Add PydanticAI adapter spike

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P2 Issue 21, P2 Issue 22

### Summary
Prototype converting deferred tools and approval-required flows from PydanticAI into `ailib` approval semantics.

### Why
PydanticAI is highly relevant for structured outputs and tool approval patterns. citeturn270580search0turn270580search2

### Scope
- map deferred tools
- map approval-required actions
- map structured validation interplay

### Deliverables
- prototype or spike document
- findings on overlap and differentiation

### Acceptance criteria
- at least one deferred/approval flow is mapped to `ailib`
- differences between tool-centric and side-effect-centric approval are documented

### Definition of done
- `ailib` has a concrete interoperability story for PydanticAI users

---

## 26) Add AutoGen adapter spike

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P2 Issue 21, P2 Issue 22

### Summary
Prototype mapping AutoGen lifecycle and persisted state into canonical `ailib` semantics.

### Why
AutoGen is strong on observability and state persistence, making it a useful interoperability target. citeturn371990search1turn371990search4

### Scope
- map state export/import concepts
- map interruption/resume equivalents
- align observability semantics where useful

### Deliverables
- prototype or spike doc
- compatibility notes

### Acceptance criteria
- one realistic lifecycle path is described or implemented
- trace/state integration opportunities are documented

### Definition of done
- `ailib` has a credible AutoGen bridge path

---

## 27) Add CrewAI adapter spike

**Suggested labels:** `priority:P2`, `type:integrations`  
**Depends on:** P2 Issue 21, P2 Issue 22

### Summary
Prototype mapping CrewAI flow-level human-in-the-loop or interruption semantics into `ailib`.

### Why
CrewAI is relevant for productized workflow adoption and enterprise-friendly agent flows. citeturn712363search0turn712363search4

### Scope
- map flow triggers into interruptions
- document compatibility assumptions
- identify where `ailib` adds stricter approval semantics

### Deliverables
- prototype or spike doc
- findings and next steps

### Acceptance criteria
- at least one realistic interruption pattern is covered
- differentiation between orchestration and supervision substrate is explicit

### Definition of done
- CrewAI users have a documented path to adopt `ailib`

---

## 28) Add action risk model

**Suggested labels:** `priority:P2`, `type:policy`  
**Depends on:** P0 Issue 10

### Summary
Define a risk/severity model for approval-relevant actions.

### Why
Policy-driven approvals require a consistent risk vocabulary.

### Scope
- low/medium/high/critical or equivalent classes
- default classification guidance
- metadata fields
- examples

### Deliverables
- risk model
- docs/examples

### Acceptance criteria
- common action categories can be classified consistently
- risk model is usable by future policy hooks and UIs

### Definition of done
- approval workflows have a common severity language

---

## 29) Add pre-approval policy hook

**Suggested labels:** `priority:P2`, `type:policy`  
**Depends on:** P2 Issue 28

### Summary
Allow a policy layer to intercept proposed actions before approval or execution.

### Why
Policy-aware control is key for real-world automation governance.

### Scope
- hook API
- allow/deny/annotate behavior
- docs/examples
- tests

### Deliverables
- pre-approval policy hook
- docs
- tests

### Acceptance criteria
- policy layer can force human approval, deny, or annotate requests deterministically
- policy results are visible in artifacts/transcripts

### Definition of done
- governance can shape approval flow before operator action

---

## 30) Add post-decision policy hook

**Suggested labels:** `priority:P2`, `type:policy`  
**Depends on:** P2 Issue 29

### Summary
Allow policy validation after approval but before final execution/resume.

### Why
Context may change after approval, and execution should still be gateable.

### Scope
- post-decision hook API
- block/annotate semantics
- docs/examples
- tests

### Deliverables
- post-decision policy hook
- docs
- tests

### Acceptance criteria
- an approved action can still be blocked intentionally by post-decision policy
- results are recorded explicitly

### Definition of done
- approvals are safer in dynamic environments

---

## 31) Add signed approval attestations

**Suggested labels:** `priority:P3`, `type:security`  
**Depends on:** P0 Issue 11, P0 Issue 15

### Summary
Add a way to sign or integrity-tag approval decisions for stronger audit confidence.

### Why
If `ailib` is used in high-risk automation, approval provenance matters.

### Scope
- attestation metadata model
- signing/integrity strategy
- verification notes

### Deliverables
- signed attestation design or implementation
- docs/examples

### Acceptance criteria
- approval provenance can be recorded in a way that is stronger than plain text logging
- guarantee boundaries are documented honestly

### Definition of done
- audit records can prove more than “someone typed approve”

---

## 32) Add transcript integrity verification tool

**Suggested labels:** `priority:P3`, `type:security`, `type:cli`  
**Depends on:** P2 Issue 15, P3 Issue 31

### Summary
Provide a CLI tool to verify tamper-evident transcript chains.

### Why
Audit trails become much more credible when they can be verified independently.

### Scope
- verification CLI
- integrity chain docs
- example transcripts

### Deliverables
- verification tool
- docs/examples

### Acceptance criteria
- integrity chain validation works on generated transcripts
- tampered examples fail verification clearly

### Definition of done
- transcript integrity can be checked offline

---

## 33) Add approval-as-code config draft

**Suggested labels:** `priority:P3`, `type:policy`, `type:standards`  
**Depends on:** P2 Issue 28, P2 Issue 29

### Summary
Draft a declarative configuration model for approval requirements and policy rules.

### Why
Approval-as-code could become one of the biggest future differentiators for enterprise adoption.

### Scope
- config schema draft
- policy examples
- required metadata rules
- simulation/preview requirements if applicable

### Deliverables
- config draft/spec
- examples
- docs

### Acceptance criteria
- at least several realistic approval policy scenarios can be expressed declaratively
- future engine integration path is clear

### Definition of done
- the project has a concrete policy-as-code direction

---

## 34) Add language-neutral protocol draft

**Suggested labels:** `priority:P3`, `type:standards`, `type:protocol`  
**Depends on:** P0 Issue 6, P2 Issue 21

### Summary
Publish a language-neutral draft of the interruption / approval / resume protocol.

### Why
Long-term category leadership requires the protocol to outgrow Python-only assumptions.

### Scope
- language-neutral schema wording
- transport independence notes
- non-Python compatibility guidance

### Deliverables
- protocol draft doc
- examples
- compatibility notes

### Acceptance criteria
- document avoids Python-only semantics where unnecessary
- external runtime implementers can understand the core contract

### Definition of done
- `ailib` begins evolving from library toward protocol standard

---

## 35) Add protocol conformance fixtures

**Suggested labels:** `priority:P3`, `type:standards`, `type:testing`  
**Depends on:** P3 Issue 34

### Summary
Create shared fixtures that third-party implementations can use to validate protocol conformance.

### Why
A standard is much stronger when others can test against it.

### Scope
- canonical fixtures
- success/failure cases
- fixture docs

### Deliverables
- conformance fixture set
- docs

### Acceptance criteria
- fixtures cover representative interruption, approval, and resume flows
- external implementers can use them without reading internal code

### Definition of done
- the protocol becomes easier to adopt beyond the reference implementation

---

## 36) Add reference architecture paper

**Suggested labels:** `priority:P3`, `type:docs`, `type:standards`  
**Depends on:** P3 Issue 34

### Summary
Write a reference architecture document explaining why interruption / approval / resume deserves a standalone layer.

### Why
Category leadership depends on clear articulation, not just code.

### Scope
- problem framing
- market gap
- architecture principles
- comparison to adjacent frameworks
- adoption guidance

### Deliverables
- architecture paper/doc

### Acceptance criteria
- document explains the value proposition clearly to technical decision-makers
- relationship to broader agent ecosystems is explicit

### Definition of done
- the project has a strong narrative asset for adoption and standardization

---

## Suggested opening order

Open in this order:

1. Implement in-memory checkpoint store
2. Implement filesystem checkpoint store
3. Implement SQLite checkpoint store
4. Add replay from checkpoint
5. Add fork-from-checkpoint support
6. Add checkpoint lineage graph export
7. Add nested interruption support
8. Add resumable partial-output semantics
9. Add pre-commit preview abstraction
10. Add idempotency key support for protected side effects
11. Add lifecycle event taxonomy
12. Add pluggable event sink interface
13. Add transcript redaction hooks
14. Add `ailib-host edit`
15. Add operator TUI pending queue
16. Add transcript timeline viewer
17. Add adapter interface for interruption emitters and resumption consumers
18. Add adapter compatibility test harness
19. Add LangGraph adapter spike
20. Add OpenAI Agents SDK adapter spike
21. Add PydanticAI adapter spike
22. Add AutoGen adapter spike
23. Add CrewAI adapter spike
24. Add action risk model
25. Add pre-approval policy hook
26. Add post-decision policy hook
27. Add signed approval attestations
28. Add transcript integrity verification tool
29. Add approval-as-code config draft
30. Add language-neutral protocol draft
31. Add protocol conformance fixtures
32. Add reference architecture paper
