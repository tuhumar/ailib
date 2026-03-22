# Open roadmap issues with GitHub CLI

This file provides copy/paste-ready `gh issue create` commands for the roadmap issue drafts.

## Assumptions

- repository: `tuhumar/ailib`
- GitHub CLI authenticated
- optional labels may be created later; remove `--label ...` flags if labels do not exist yet

## P0 / P1

### 1. Audit actual repository capabilities

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Audit actual repository capabilities" \
  --body-file <(cat <<'EOF'
Create a single source of truth for what `ailib` actually implements today versus what is only documented or planned.

## Why
The repository currently appears to be in a transitional state. Before building toward world-class interruption / approval / resume, the project needs one honest capability baseline.

## Scope
- inventory exported API surface
- inventory actual modules and stable entry points
- compare code vs README vs CONTRIBUTING vs CHANGELOG vs examples
- classify each capability as implemented, partial, planned, or drifted/inaccurate

## Deliverables
- `docs/status.md` or equivalent capability matrix
- concise drift summary
- recommended corrective actions

## Acceptance criteria
- every public symbol is accounted for
- every documented feature is tagged by real status
- major drift areas are explicit
- output is good enough to guide README/version cleanup
EOF
) \
  --label priority:P0 --label type:docs
```

### 2. Rewrite README around real product state

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Rewrite README around real product state" \
  --body-file <(cat <<'EOF'
Rewrite `README.md` so it matches the actual state of the codebase and clearly distinguishes shipped, experimental, and planned functionality.

## Depends on
- Audit actual repository capabilities

## Scope
- validate install steps
- validate quickstart
- validate examples
- label stable vs experimental features
- align terminology around interruption / approval / resume

## Acceptance criteria
- setup works from a clean environment
- documented commands run as written
- terminology is consistent with roadmap/backlog
- no absent feature is described as shipped
EOF
) \
  --label priority:P0 --label type:docs
```

### 3. Restore or add CI at repository root

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Restore or add CI at repository root" \
  --body-file <(cat <<'EOF'
Ensure the repository has a working root-level CI workflow that validates tests, build, lint, and typing.

## Scope
- test suite execution
- build validation
- lint
- typing
- supported Python version matrix

## Acceptance criteria
- CI runs on pushes and PRs
- CI validates package build
- CI fails on test/lint/type errors
- documented local commands match CI steps
EOF
) \
  --label priority:P0 --label type:testing --label type:release
```

### 4. Finalize top-level convenience API

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Finalize top-level convenience API" \
  --body-file <(cat <<'EOF'
Freeze and document the intended top-level convenience API for `ask`, `decide`, and `ask_json`.

## Scope
- finalize function signatures
- normalize parameter names
- define timeout semantics
- define metadata semantics
- define exception behavior

## Acceptance criteria
- all convenience functions behave consistently
- timeout handling is documented and tested
- metadata behavior is explicit
- semver-sensitive API decisions are recorded
EOF
) \
  --label priority:P0 --label type:api
```

### 5. Introduce explicit `Client` contract

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Introduce explicit Client contract" \
  --body-file <(cat <<'EOF'
Define and document `Client` as the explicit wiring path for applications that do not want global convenience state.

## Depends on
- Finalize top-level convenience API

## Scope
- define responsibilities of `Client`
- define relationship between `Client` and global helpers
- document explicit usage patterns
- add tests for direct `Client` usage

## Acceptance criteria
- `Client` behavior is documented and tested
- convenience API delegates predictably to `Client`
- explicit and implicit usage paths are both supported intentionally
EOF
) \
  --label priority:P0 --label type:api
```

### 6. Define envelope schema set

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Define envelope schema set" \
  --body-file <(cat <<'EOF'
Define the canonical schema set for request, interruption, resume, and response lifecycles.

## Depends on
- Finalize top-level convenience API
- Introduce explicit Client contract

## Scope
- `RequestEnvelope`
- `InterruptionEnvelope`
- `ResumeEnvelope`
- `ResponseEnvelope`
- schema versioning strategy
- example wire payloads

## Acceptance criteria
- all core lifecycles map onto one envelope family
- fields are named consistently
- sample payloads exist for all major flows
- schema versioning rules are documented
EOF
) \
  --label priority:P0 --label type:protocol
```

### 7. Define canonical identifiers

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Define canonical identifiers" \
  --body-file <(cat <<'EOF'
Define the ID model for correlating runs, threads, requests, approvals, and checkpoints.

## Depends on
- Define envelope schema set

## Scope
- `run_id`
- `thread_id`
- `request_id`
- `approval_id`
- `checkpoint_id`
- generation rules
- propagation rules

## Acceptance criteria
- each ID has clear lifecycle semantics
- logs/transcripts can correlate on IDs
- IDs are not ambiguous across resume/replay paths
EOF
) \
  --label priority:P0 --label type:protocol
```

### 8. Define action kinds and statuses

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Define action kinds and statuses" \
  --body-file <(cat <<'EOF'
Define the canonical action kinds and lifecycle statuses for interruption and approval flows.

## Depends on
- Define envelope schema set

## Scope
- action kinds for question, approval, edit_request, provide_input, external_result, cancel, error
- statuses for pending, approved, rejected, edited, cancelled, expired, failed, completed
- transition rules

## Acceptance criteria
- kinds and statuses cover core use cases
- illegal transitions are documented or prevented
- host-side semantics are clear
EOF
) \
  --label priority:P0 --label type:protocol
```

### 9. Design checkpoint store interface

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Design checkpoint store interface" \
  --body-file <(cat <<'EOF'
Design the pluggable interface for saving and restoring paused execution state.

## Depends on
- Define envelope schema set
- Define canonical identifiers

## Scope
- create checkpoint
- get checkpoint
- list checkpoints
- resume checkpoint
- fork checkpoint
- metadata/versioning

## Acceptance criteria
- interface supports at least memory, filesystem, SQLite, and Postgres implementations in future
- checkpoint metadata includes enough information for resume and replay
- API is transport-agnostic
EOF
) \
  --label priority:P0 --label type:persistence
```

### 10. Design approval schema

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Design approval schema" \
  --body-file <(cat <<'EOF'
Design the structured approval object used across all high-risk or human-gated actions.

## Depends on
- Define envelope schema set
- Define action kinds and statuses

## Scope
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

## Acceptance criteria
- approvals are portable across terminal, UI, and external integrations
- edit-and-approve is representable
- expiration and stale decisions are representable
EOF
) \
  --label priority:P0 --label type:protocol
```

### 11. Add transcript schema

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Add transcript schema" \
  --body-file <(cat <<'EOF'
Define the transcript format used to record interruption, approval, resume, checkpoint, and error lifecycles.

## Depends on
- Define envelope schema set
- Define canonical identifiers

## Scope
- transcript event schema
- correlation IDs
- actor metadata
- timestamps
- status transitions
- error representation
- redaction hooks design notes

## Acceptance criteria
- transcript can reconstruct the lifecycle of a run
- transcript includes enough correlation to support replay/debugging later
- transcript format is append-friendly and tooling-friendly
EOF
) \
  --label priority:P1 --label type:observability
```

### 12. Add `ailib-host inspect`

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Add ailib-host inspect" \
  --body-file <(cat <<'EOF'
Add the first host CLI command to inspect pending interruptions, requests, or checkpoints clearly from the terminal.

## Depends on
- Define envelope schema set
- Design approval schema
- Add transcript schema

## Scope
- inspect request file or interruption artifact
- render rich human-readable view
- show IDs, status, kind, summary, risk, metadata, and relevant payloads
- support raw JSON output mode

## Acceptance criteria
- command can inspect at least one canonical artifact format
- output is clear enough to support manual supervision
- raw mode supports automation/debugging
EOF
) \
  --label priority:P1 --label type:cli
```

### 13. Add legacy compatibility parser

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Add legacy compatibility parser" \
  --body-file <(cat <<'EOF'
Add a clearly bounded compatibility parser for legacy raw-string and legacy-object workflows.

## Depends on
- Define envelope schema set
- Define action kinds and statuses

## Scope
- raw string compatibility where intended
- legacy object compatibility where intended
- disambiguation rules
- bounded scope documentation

## Acceptance criteria
- compatibility behavior is deterministic
- parser does not silently reinterpret canonical payloads incorrectly
- unsupported legacy shapes fail clearly
EOF
) \
  --label priority:P1 --label type:protocol
```

### 14. Add OpenTelemetry-compatible event hooks

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Add OpenTelemetry-compatible event hooks" \
  --body-file <(cat <<'EOF'
Expose lifecycle hooks that can feed OpenTelemetry-compatible tracing without binding the library to a specific vendor.

## Depends on
- Define canonical identifiers
- Add transcript schema

## Scope
- lifecycle event taxonomy
- hook interface
- span-friendly metadata
- correlation ID propagation

## Acceptance criteria
- interruption/approval/resume lifecycles emit structured events
- events include correlation IDs
- hooks can be no-op by default
EOF
) \
  --label priority:P1 --label type:observability
```

### 15. Add transcript logger

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Add transcript logger" \
  --body-file <(cat <<'EOF'
Implement a transcript logger that writes lifecycle events to an append-friendly local format, such as JSONL.

## Depends on
- Add transcript schema

## Scope
- local transcript sink
- file rotation/basic safety notes
- correlation IDs
- event serialization
- optional redaction hooks

## Acceptance criteria
- a real run can generate a readable transcript
- transcript contains enough data to inspect what paused and why
- logger can be enabled without invasive wiring
EOF
) \
  --label priority:P1 --label type:observability
```

### 16. Add CLI commands for approve / reject / resume

```bash
gh issue create \
  --repo tuhumar/ailib \
  --title "Add CLI commands for approve reject and resume" \
  --body-file <(cat <<'EOF'
Add the next host CLI commands that allow supervisors to resolve interruptions from the terminal.

## Depends on
- Design approval schema
- Add ailib-host inspect

## Scope
- `ailib-host approve`
- `ailib-host reject`
- `ailib-host resume`
- optional structured edit support later

## Acceptance criteria
- host can approve, reject, or resume using canonical artifacts
- resulting artifacts are protocol-valid
- failure/error flows are handled clearly
EOF
) \
  --label priority:P1 --label type:cli
```

## Remaining backlog

For the rest of the roadmap, use the issue bodies in:

- `ISSUE_DRAFTS_P2_P3.md`

If you want, convert the same pattern above for each P2/P3 issue or wrap them in a shell script that iterates over markdown body files.
