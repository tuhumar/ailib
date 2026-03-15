from __future__ import annotations

import json
import os
import tempfile
from typing import Any


def ensure_parent_dir(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def write_json_atomic(path: str, payload: dict[str, Any]) -> None:
    ensure_parent_dir(path)
    temp_dir = os.path.dirname(path) or "."
    fd, temp_path = tempfile.mkstemp(prefix=".ailib_", suffix=".json.tmp", dir=temp_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
        os.replace(temp_path, path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def read_json_or_text(path: str) -> dict[str, Any] | str | None:
    with open(path, "r", encoding="utf-8") as handle:
        raw = handle.read().strip()
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(parsed, dict):
        return parsed
    return raw
