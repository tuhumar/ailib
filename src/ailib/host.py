from __future__ import annotations

import json
import os
import sys

from .backends.stdio import (
    REQUEST_END_MARKER,
    REQUEST_START_MARKER,
    RESPONSE_END_MARKER,
    RESPONSE_START_MARKER,
    extract_delimited_payload,
    format_delimited_payload,
)
from .exceptions import ProtocolError
from .io_utils import read_json_or_text, write_json_atomic
from .models import RequestEnvelope, ResponseEnvelope, ResponseStatus


def read_file_request(path: str) -> RequestEnvelope | None:
    if not os.path.exists(path):
        return None
    payload = read_json_or_text(path)
    if payload is None:
        return None
    if isinstance(payload, str):
        return None
    return RequestEnvelope.from_dict(payload)


def write_file_response(path: str, response: ResponseEnvelope) -> None:
    write_json_atomic(path, response.to_dict())


def write_file_response_ok(path: str, request_id: str, output: str, metadata=None) -> None:
    response = ResponseEnvelope(
        request_id=request_id,
        status=ResponseStatus.OK,
        output=output,
        metadata=dict(metadata or {}),
    )
    write_file_response(path, response)


def write_file_response_error(path: str, request_id: str, error: str, metadata=None) -> None:
    response = ResponseEnvelope(
        request_id=request_id,
        status=ResponseStatus.ERROR,
        error=error,
        metadata=dict(metadata or {}),
    )
    write_file_response(path, response)


def write_file_response_cancelled(path: str, request_id: str, error: str, metadata=None) -> None:
    response = ResponseEnvelope(
        request_id=request_id,
        status=ResponseStatus.CANCELLED,
        error=error,
        metadata=dict(metadata or {}),
    )
    write_file_response(path, response)


def parse_stdio_request(text: str) -> RequestEnvelope | None:
    payload = extract_delimited_payload(text, REQUEST_START_MARKER, REQUEST_END_MARKER)
    if payload is None:
        return None
    parsed = _load_delimited_mapping(payload, label="stdio request")
    return RequestEnvelope.from_dict(parsed)


def read_stdio_request(stream=None) -> RequestEnvelope | None:
    source = stream if stream is not None else sys.stdin
    text = source.read()
    if not text:
        return None
    return parse_stdio_request(text)


def format_stdio_response(response: ResponseEnvelope) -> str:
    payload = json.dumps(response.to_dict(), indent=2, ensure_ascii=False)
    return format_delimited_payload(payload, RESPONSE_START_MARKER, RESPONSE_END_MARKER)


def write_stdio_response(response: ResponseEnvelope, stream=None) -> None:
    target = stream if stream is not None else sys.stdout
    target.write(format_stdio_response(response))
    target.flush()


def write_stdio_response_ok(request_id: str, output: str, stream=None, metadata=None) -> None:
    response = ResponseEnvelope(
        request_id=request_id,
        status=ResponseStatus.OK,
        output=output,
        metadata=dict(metadata or {}),
    )
    write_stdio_response(response, stream=stream)


def write_stdio_response_error(request_id: str, error: str, stream=None, metadata=None) -> None:
    response = ResponseEnvelope(
        request_id=request_id,
        status=ResponseStatus.ERROR,
        error=error,
        metadata=dict(metadata or {}),
    )
    write_stdio_response(response, stream=stream)


def write_stdio_response_cancelled(request_id: str, error: str, stream=None, metadata=None) -> None:
    response = ResponseEnvelope(
        request_id=request_id,
        status=ResponseStatus.CANCELLED,
        error=error,
        metadata=dict(metadata or {}),
    )
    write_stdio_response(response, stream=stream)


def _load_delimited_mapping(payload: str, label: str) -> dict:
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ProtocolError(f"Invalid {label} JSON payload: {exc}.") from exc
    if not isinstance(parsed, dict):
        raise ProtocolError(f"{label.title()} payload must decode to a JSON object.")
    return parsed
