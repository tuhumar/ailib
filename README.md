# ailib

`ailib` is a small Python library for agent-in-the-loop workflows where a running script needs to stop, ask for help, and wait for a structured response from a supervising agent.

This rewrite focuses on three things:

- explicit protocol envelopes instead of ad-hoc payloads
- typed backends with predictable errors
- a clean split between script-side client code and host-side response helpers

## What it provides

- `Client` for direct use in applications
- global convenience functions: `ask`, `decide`, `ask_json`, `ask_model`
- `StdioBackend` for terminal-driven agents
- `FileBackend` for file/IPC workflows
- typed request/response envelopes with `request_id`
- host helpers for reading file requests and writing file responses
- lazy global context with `reset_context()` for tests and embedding scenarios

## Install

```bash
pip install -e .
```

For local development with the optional validation dependencies:

```bash
pip install -e .[dev]
```

With Pydantic support:

```bash
pip install -e .[pydantic]
```

With full JSON Schema validation support:

```bash
pip install -e .[schema]
```

## Quick start

```python
import ailib

summary = ailib.ask("Summarize the current task.", context={"files": ["main.py"]})
decision = ailib.decide("What should I do next?", options=["retry", "abort", "ignore"])
```

For JSON:

```python
payload = ailib.ask_json("Return a JSON object with a title and a score.")
```

You can also validate the returned JSON locally against a schema:

```python
payload = ailib.ask_json(
    "Return a JSON object with status and score.",
    schema={
        "type": "object",
        "required": ["status", "score"],
        "properties": {
            "status": {"type": "string", "const": "ok"},
            "score": {"type": "integer", "minimum": 1},
        },
        "additionalProperties": False,
    },
)
```

For Pydantic models:

```python
from pydantic import BaseModel
import ailib

class Plan(BaseModel):
    action: str
    eta_minutes: int

plan = ailib.ask_model("Propose the next action.", Plan)
```

## API overview

### Client-side API

- `Client(backend)` for explicit application wiring
- `ask(prompt, context=None, timeout_s=None, metadata=None)`
- `decide(prompt, options, context=None, timeout_s=None, metadata=None)`
- `ask_json(prompt, context=None, timeout_s=None, metadata=None, schema=None)`
- `ask_model(prompt, model_cls, context=None, timeout_s=None, metadata=None)`

### Context helpers

- `get_client()` lazily builds the default client from environment variables
- `set_client(client)` replaces the cached global client
- `set_backend(backend)` wraps a backend in a `Client` and caches it
- `reset_context()` clears the cached client so the next convenience call rebuilds it from env
- `use_backend(backend)` temporarily swaps the cached backend inside a context manager

### Host-side helpers

- file mode: `read_file_request()`, `write_file_response_*()`
- stdio mode: `parse_stdio_request()`, `read_stdio_request()`, `write_stdio_response_*()`

## Protocol

### Request envelope

Every interaction is serialized as a request envelope with:

- `protocol_version`
- `request_id`
- `kind`
- `prompt`
- `context`
- `options`
- `schema`
- `timeout_s`
- `metadata`
- `created_at`

### Response envelope

Structured responses may include:

- `protocol_version`
- `request_id`
- `status`
- `output`
- `error`
- `metadata`
- `responded_at`

Incoming envelopes validate `protocol_version` by major version. `2.x` is accepted; incompatible majors raise `ProtocolError`.

### Compatibility rules

- raw text responses are accepted for simple `ask` / `decide`
- raw JSON objects/arrays are accepted for `ask_json` / `ask_model`
- `{"response": "..."}` remains accepted for legacy string workflows
- full response envelopes remain the canonical structured format

## Backends

### `StdioBackend`

Emits a JSON request envelope to `stderr` between these markers:

```text
<<<AILIB_REQUEST_START>>>
{...}
<<<AILIB_REQUEST_END>>>
```

The host agent should answer on `stdin`. It can send:

- a raw text line
- a JSON object like `{"output": "retry"}`
- a full response envelope

For multiline JSON responses, the host can delimit them with response markers:

```text
<<<AILIB_RESPONSE_START>>>
{...}
<<<AILIB_RESPONSE_END>>>
```

### `FileBackend`

Writes a request envelope to `request.json` and waits for `response.json`.

The response file may contain:

- a raw string
- `{"response": "..."}` for legacy compatibility
- a full response envelope

Every request carries a `request_id`, and the backend ignores mismatched responses.
Incoming envelopes also validate `protocol_version` by major version, so `2.x` stays compatible while `1.x` or `3.x` are rejected.

## Environment variables

- `AILIB_BACKEND`: `stdio`, `stdin`, or `file`
- `AILIB_TIMEOUT`: default timeout in seconds
- `AILIB_FILE_REQUEST`: request path for `FileBackend`
- `AILIB_FILE_RESPONSE`: response path for `FileBackend`
- `AILIB_STDIN_FILE`: optional fallback file consumed by `StdioBackend`

## Host-side helpers

`ailib.host` contains small utilities for the supervising agent.

For file-based workflows:

```python
from ailib.host import read_file_request, write_file_response_cancelled, write_file_response_ok

request = read_file_request("request.json")
if request is not None:
    cancel = False
    if cancel:
        write_file_response_cancelled("response.json", request_id=request.request_id, error="cancelled by host")
    else:
        write_file_response_ok("response.json", request_id=request.request_id, output="approved")
```

For stdio-based workflows:

```python
import sys
from ailib.host import parse_stdio_request, write_stdio_response_ok

request = parse_stdio_request(captured_stderr_text)
if request is not None:
    write_stdio_response_ok(request.request_id, "approved", stream=sys.stdout)
```

## Testing

```bash
PYTHONPATH=src python3 -m unittest discover tests
```

## Build

Standard release build:

```bash
python3 -m build
```

If build dependencies are already present locally, you can also validate packaging without isolated bootstrap:

```bash
python3 -m build --no-isolation
```

This repository also includes a minimal CI workflow at `.github/workflows/ci.yml` for Python 3.10, 3.11 and 3.12.

If `ailib` is still kept as a subdirectory inside a larger repository, that workflow is only a template: GitHub Actions will only execute workflows that live at the parent repository root. Move or mirror it to the real root when wiring CI in the current git repository.

If you rely on the global convenience API in a long-lived process, `reset_context()` clears the cached client so the next call rebuilds it from environment variables.

## Examples

- `examples/simple_task.py`: minimal file backend flow
- `examples/codex_stdio_demo.py`: interactive stdio prompt for manual validation
- `examples/file_roundtrip_demo.py`: self-contained file backend roundtrip with host thread and JSON log written to a temporary directory
- `examples/stdio_roundtrip_simulated.py`: self-contained stdio roundtrip with simulated host and JSON log written to a temporary directory

## Errors

The public exceptions are:

- `ConfigurationError`
- `ProtocolError`
- `TransportError`
- `AILibTimeoutError`
- `RequestCancelledError`
- `RemoteExecutionError`
- `InvalidChoiceError`
- `InvalidJSONError`
- `SchemaValidationError`

## Repository layout

- `src/ailib/`: library code
- `tests/`: unit and integration coverage
- `examples/`: runnable examples
- `CONTRIBUTING.md`: local workflow for contributors
- `CHANGELOG.md`: library evolution summary
- `LICENSE`: MIT license text
