# Roadmap research updates

This document captures additional roadmap corrections and future bets based on recent review of adjacent ecosystems.

## Main findings from current ecosystem research

### 1. Durable pause/resume is a category requirement
Projects in the space increasingly treat interruption as durable state, not just a synchronous prompt/response exchange.

Implication for `ailib`:
- elevate `run_id`, `thread_id`, and checkpoint-oriented thinking in the roadmap
- prioritize resumable state over transport-only features

### 2. Human-in-the-loop needs serialization, not just callbacks
Modern HITL systems expose serializable run state and long-running approval flows.

Implication for `ailib`:
- strengthen roadmap emphasis on resumable interruption records
- add approval objects that survive process boundaries
- design for deferred approval and late resume

### 3. Tracing is now a baseline differentiator
Leading SDKs increasingly ship built-in trace/event models instead of leaving observability fully to users.

Implication for `ailib`:
- move event taxonomy and trace correlation closer to the core roadmap
- standardize `request_id`, `run_id`, and `thread_id` usage across logs, transcripts, and envelopes

### 4. Replay and idempotency matter more than generic orchestration
The strongest platforms focus on deterministic resume, side-effect safety, and replay semantics.

Implication for `ailib`:
- keep the product focused on interruption / approval / resume
- avoid expanding into a generic multi-agent framework too early
- prioritize side-effect safety, replay, and approval diffs

## Roadmap corrections to emphasize

### Raise priority of these items
- correlation identifiers in protocol models
- checkpoint-oriented persistence interfaces
- transcript/event schema
- host/operator tooling for inspection and manual resume
- compatibility-safe protocol evolution

### Keep these as later-stage items
- broad orchestration features
- large framework-like abstractions inside core
- transport sprawl before persistence and resume semantics are solid

## Additional future bets

- approval diff protocol for code, files, SQL, and shell actions
- portable interruption record format for non-Python runtimes
- policy-aware approvals and risk levels
- replay/fork lineage for audit and debugging
- operator inbox concepts for future CLI/TUI/web surfaces

## Recommended near-term order after current alignment work

1. stabilize CI/smoke and build validation
2. tighten protocol/correlation identifiers
3. improve durable request/response semantics
4. add transcript/event foundations
5. add host inspection/resume tooling
6. add persistence/checkpoint abstractions
7. expand compatibility and observability

This document should be read as an addendum to the main roadmap and execution backlog, not as a replacement for them.
