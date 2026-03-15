# Contributing

## Local setup

```bash
pip install -e .[dev]
```

If you want a narrower install, the optional extras can also be installed independently:

```bash
pip install -e .
pip install -e .[pydantic]
pip install -e .[schema]
```

## Test suite

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest discover tests
```

## Build artifacts

Standard release build:

```bash
python3 -m build
```

If build dependencies are already installed locally and you want to avoid isolated environment bootstrap:

```bash
python3 -m build --no-isolation
```

## CI

A minimal GitHub Actions workflow is provided at `.github/workflows/ci.yml`. When `ailib` is used as a standalone repository root, it runs:

- the unittest suite on Python 3.10, 3.11 and 3.12
- editable install with `pydantic` and `schema` extras
- `python -m build` for sdist/wheel validation

If `ailib` remains nested inside another repository, move or mirror that workflow to the parent repository root before expecting GitHub Actions to execute it.

## Scope

- Keep `ailib` independent from application-specific code.
- Preserve request/response envelopes with `request_id`.
- Prefer explicit `Client`/backend usage over hidden bootstrap in examples and integration code.
- Maintain compatibility with the documented legacy payloads only where already supported.
