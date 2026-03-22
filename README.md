# ailib

`ailib` is a Python library for **agent-in-the-loop / supervised execution** workflows.

It is designed for programs that need to:

- stop at a meaningful point,
- ask a supervising host for input or a decision,
- receive a structured response,
- continue execution with less guesswork and better control.

Today, the public repository already provides a usable core for that workflow. At the same time, the project is in an active **alignment and maturation phase**: some public docs describe a more advanced target architecture than the minimum set a new contributor can safely assume is finished.

This README is intentionally centered on the **real repository state** and the **verified public API direction**.

---

## What `ailib` is good for

Typical use cases include:

- scripts that need human or supervisor input mid-run
- code or automation flows that need a clear pause/continue point
- structured JSON responses instead of free-form text only
- simple host-driven workflows over `stdio` or file-based request/response exchange
- experiments in supervised agent execution without committing to a full orchestration framework

---

## What exists in the public API today

The current repository exposes a public shape built around:

- an explicit `Client` abstraction
- top-level convenience helpers:
  - `ask()`
  - `decide()`
  - `ask_json()`
  - `ask_model()`
- context helpers:
  - `get_client()`
  - `set_client()`
  - `set_backend()`
  - `reset_context()`
  - `use_backend()`
- backend-oriented workflows for `stdio` / `stdin` and file-based exchange
- structured parsing helpers for JSON and model-shaped output

The project direction also clearly points toward a stronger interruption protocol, richer host tooling, and more durable pause/resume semantics, but contributors should treat those as **active roadmap work unless they are visible and validated in the branch they are using**.

---

## Install

Editable local install:

```bash
pip install -e .
```

Optional extras:

```bash
pip install -e .[dev]
pip install -e .[pydantic]
pip install -e .[schema]
```

---

## Quick start

### Convenience API

```python
import ailib

summary = ailib.ask("Summarize the current task.", context={"files": ["main.py"]})
next_step = ailib.decide(
    "What should happen next?",
    options=["retry", "abort", "ignore"],
)
payload = ailib.ask_json("Return a JSON object with a title and a score.")
```

### Model-shaped output

```python
from pydantic import BaseModel
import ailib

class Plan(BaseModel):
    action: str
    eta_minutes: int

plan = ailib.ask_model("Propose the next action.", Plan)
```

---

## Backend selection

`ailib` builds its default client from environment variables.

Relevant variables include:

- `AILIB_BACKEND`: `stdio`, `stdin`, or `file`
- `AILIB_TIMEOUT`: default timeout in seconds
- `AILIB_FILE_REQUEST`: request path for file backend flows
- `AILIB_FILE_RESPONSE`: response path for file backend flows
- `AILIB_STDIN_FILE`: optional fallback file for stdin-oriented flows

In practice, this means you can keep the convenience API in application code and switch transport behavior from the environment.

---

## Public API overview

### Main entry points

- `Client(backend)`
- `ask(prompt, context=None, timeout_s=None, metadata=None)`
- `decide(prompt, options, context=None, timeout_s=None, metadata=None)`
- `ask_json(prompt, context=None, timeout_s=None, metadata=None, schema=None)`
- `ask_model(prompt, model_cls, context=None, timeout_s=None, metadata=None)`

### Context helpers

- `get_client()`
- `set_client(client)`
- `set_backend(backend)`
- `reset_context(client=None)`
- `use_backend(backend)`

### Host-side direction

The repository also exposes host-side helpers and protocol-oriented utilities. These are part of the intended architecture, but contributors should validate exact helper names and workflow guarantees against the branch they are using when building new integrations.

---

## Current project maturity

The safest way to think about `ailib` today is:

### Implemented / visible direction

- explicit client + convenience API
- environment-driven backend selection
- `stdio` and file-oriented workflow support
- JSON / model-oriented structured response handling
- a clear move toward request/response envelope-based interaction

### Active alignment areas

- exact protocol maturity claims
- repository truth vs changelog/README/version narrative
- CI and release-discipline consistency
- stronger operator tooling and persistence guarantees

### Roadmap direction, not baseline guarantee

These are active roadmap themes and should not be assumed to be fully shipped unless verified in the branch you are using:

- world-class interruption / approval / resume semantics
- durable checkpointing and cross-process resume
- replay / fork / lineage support
- operator inbox / TUI / external approval bridges
- policy-driven approvals and audit-grade supervision
- framework adapters for larger agent ecosystems

---

## Examples

The repository currently includes at least this directly runnable example:

- `examples/simple_task.py`

That example is a good starting point for understanding the convenience API in a small interactive flow.

If other docs or roadmap files mention deeper examples, treat them as branch-dependent until verified in the repository state you are using.

---

## Testing

Run the current test suite with:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover tests
```

---

## Build

Build the package with:

```bash
python3 -m build
```

If build dependencies are already installed locally:

```bash
python3 -m build --no-isolation
```

---

## Errors

Public exceptions documented by the repository include:

- `ConfigurationError`
- `ProtocolError`
- `TransportError`
- `AILibTimeoutError`
- `RequestCancelledError`
- `RemoteExecutionError`
- `InvalidChoiceError`
- `InvalidJSONError`
- `SchemaValidationError`

As the protocol and API continue to harden, contributors should prefer these domain-specific errors over broad generic exceptions.

---

## Repository layout

- `src/ailib/` — library code
- `tests/` — automated coverage
- `examples/` — runnable examples
- `CONTRIBUTING.md` — contributor workflow notes
- `CHANGELOG.md` — change history
- `LICENSE` — license text

---

## Direction

The long-term ambition for `ailib` is larger than the current baseline:

- a stronger interruption contract
- richer approvals
- cleaner resume semantics
- durable state and replay
- better operator tooling
- better interoperability with broader agent ecosystems

But the project will get there most credibly by staying honest about what is already implemented, what is partial, and what is still roadmap work.

That is the frame this README follows.
