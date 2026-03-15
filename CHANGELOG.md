# Changelog

## [2.0.0] - Refactor

- Rebuilt the library around explicit request and response envelopes.
- Added a typed `Client` API and host-side file helpers.
- Added strict choice validation for `decide()`.
- Added robust file backend cleanup and request id matching.
- Added compatibility parsing for legacy raw-string and `{"response": ...}` payloads.
- `Client` now enforces `error` and `cancelled` response statuses even for custom backends.
- Added a host-side helper for writing `cancelled` file responses and tests covering host helpers.
- Added local JSON schema validation for `ask_json()` responses, with optional `jsonschema` support and a built-in subset validator.
- Added host-side stdio helpers for parsing request envelopes and writing delimited stdio responses.
- `StdioBackend` now supports response markers, multiline JSON responses, and real timeouts.
- Enforced `protocol_version` compatibility by major version for incoming request and response envelopes.
- Global context initialization is now lazy, and `reset_context()` can clear or replace the cached client explicitly.
- Fixed raw JSON response disambiguation for `ask_json()` / `ask_model()` so application payloads are not mistaken for protocol envelopes.
- Added repo hygiene files: `.gitignore`, `LICENSE`, and `CONTRIBUTING.md`.
- Added runnable roundtrip examples for `FileBackend` and `StdioBackend`, both emitting JSON logs for manual inspection.
- Added automated coverage for `io_utils`, `logging_utils`, and smoke execution of the examples.
- Clarified repository documentation around the `dev` extra, temporary example logs, and the fact that the bundled GitHub Actions workflow only runs when `ailib` is the repository root.
