from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .exceptions import ProtocolError, RemoteExecutionError, RequestCancelledError


PROTOCOL_VERSION = "2.0"
PROTOCOL_MAJOR_VERSION = PROTOCOL_VERSION.split(".", 1)[0]


class InteractionKind(str, Enum):
    ASK = "ask"
    DECIDE = "decide"
    ASK_JSON = "ask_json"
    ASK_MODEL = "ask_model"


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"
    CANCELLED = "cancelled"


@dataclass
class RequestEnvelope:
    prompt: str
    kind: InteractionKind = InteractionKind.ASK
    context: Any = None
    options: list[str] | None = None
    schema: dict[str, Any] | None = None
    timeout_s: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: float = field(default_factory=time.time)
    protocol_version: str = PROTOCOL_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol_version": self.protocol_version,
            "request_id": self.request_id,
            "kind": self.kind.value,
            "prompt": self.prompt,
            "context": self.context,
            "options": self.options,
            "schema": self.schema,
            "timeout_s": self.timeout_s,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "RequestEnvelope":
        if "prompt" not in payload:
            raise ProtocolError("Request payload is missing 'prompt'.")

        protocol_version = _coerce_protocol_version(payload.get("protocol_version", PROTOCOL_VERSION), label="Request")
        return cls(
            prompt=str(payload["prompt"]),
            kind=InteractionKind(payload.get("kind", InteractionKind.ASK.value)),
            context=payload.get("context"),
            options=_coerce_options(payload.get("options")),
            schema=_coerce_mapping(payload.get("schema")),
            timeout_s=_coerce_timeout(payload.get("timeout_s")),
            metadata=_coerce_mapping(payload.get("metadata")) or {},
            request_id=str(payload.get("request_id") or uuid.uuid4().hex),
            created_at=float(payload.get("created_at", time.time())),
            protocol_version=protocol_version,
        )


@dataclass
class ResponseEnvelope:
    request_id: str
    status: ResponseStatus = ResponseStatus.OK
    output: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    responded_at: float = field(default_factory=time.time)
    protocol_version: str = PROTOCOL_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "protocol_version": self.protocol_version,
            "request_id": self.request_id,
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "metadata": self.metadata,
            "responded_at": self.responded_at,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any], fallback_request_id: str | None = None) -> "ResponseEnvelope":
        request_id = str(payload.get("request_id") or fallback_request_id or "")
        if not request_id:
            raise ProtocolError("Response payload is missing 'request_id'.")

        status_value = payload.get("status", ResponseStatus.OK.value)
        output = payload.get("output")
        if output is None and "response" in payload:
            output = payload.get("response")

        protocol_version = _coerce_protocol_version(payload.get("protocol_version", PROTOCOL_VERSION), label="Response")
        return cls(
            request_id=request_id,
            status=ResponseStatus(status_value),
            output=None if output is None else str(output),
            error=None if payload.get("error") is None else str(payload.get("error")),
            metadata=_coerce_mapping(payload.get("metadata")) or {},
            responded_at=float(payload.get("responded_at", time.time())),
            protocol_version=protocol_version,
        )

    @classmethod
    def coerce(
        cls,
        payload: Any,
        fallback_request_id: str | None = None,
        request_kind: InteractionKind | str | None = None,
    ) -> "ResponseEnvelope":
        if isinstance(payload, cls):
            return payload
        normalized_request_kind = _normalize_request_kind(request_kind)
        if isinstance(payload, dict):
            if _looks_like_response_envelope_payload(payload, request_kind=normalized_request_kind):
                return cls.from_dict(payload, fallback_request_id=fallback_request_id)
            if not fallback_request_id:
                raise ProtocolError("A raw JSON response requires a fallback request id.")
            return cls(request_id=fallback_request_id, output=json.dumps(payload, ensure_ascii=False))
        if isinstance(payload, list):
            if not fallback_request_id:
                raise ProtocolError("A raw JSON response requires a fallback request id.")
            return cls(request_id=fallback_request_id, output=json.dumps(payload, ensure_ascii=False))
        if isinstance(payload, str):
            text = payload.strip()
            if text.startswith("{") and text.endswith("}"):
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, dict):
                    if _looks_like_response_envelope_payload(parsed, request_kind=normalized_request_kind):
                        return cls.from_dict(parsed, fallback_request_id=fallback_request_id)
                    if not fallback_request_id:
                        raise ProtocolError("A raw JSON response requires a fallback request id.")
                    return cls(request_id=fallback_request_id, output=text)
            if text.startswith("[") and text.endswith("]"):
                try:
                    parsed = json.loads(text)
                except json.JSONDecodeError:
                    parsed = None
                if isinstance(parsed, list):
                    if not fallback_request_id:
                        raise ProtocolError("A raw JSON response requires a fallback request id.")
                    return cls(request_id=fallback_request_id, output=text)
            if not fallback_request_id:
                raise ProtocolError("A raw string response requires a fallback request id.")
            return cls(request_id=fallback_request_id, output=text)
        raise ProtocolError(f"Unsupported response payload type: {type(payload)!r}")

    def require_ok(self) -> "ResponseEnvelope":
        if self.status == ResponseStatus.ERROR:
            raise RemoteExecutionError(self.error or "The supervising agent returned an error.")
        if self.status == ResponseStatus.CANCELLED:
            raise RequestCancelledError(self.error or "The supervising agent cancelled the request.")
        return self


def _coerce_protocol_version(value: Any, label: str) -> str:
    version = str(value or PROTOCOL_VERSION).strip()
    if not version:
        version = PROTOCOL_VERSION
    major = version.split(".", 1)[0]
    if not major.isdigit():
        raise ProtocolError(f"{label} payload has an invalid protocol_version: {version!r}.")
    if major != PROTOCOL_MAJOR_VERSION:
        raise ProtocolError(
            f"{label} payload protocol_version {version!r} is incompatible with supported major version {PROTOCOL_MAJOR_VERSION}."
        )
    return version


def _coerce_mapping(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ProtocolError("Expected a dictionary payload.")
    return dict(value)


def _coerce_options(value: Any) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ProtocolError("Expected 'options' to be a list.")
    return [str(item) for item in value]


def _coerce_timeout(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _looks_like_response_envelope_payload(payload: dict[str, Any], request_kind: str | None = None) -> bool:
    if "request_id" in payload:
        return True

    # For ask_json/ask_model, a dict without request_id is more likely to be the raw payload.
    if request_kind in {InteractionKind.ASK_JSON.value, InteractionKind.ASK_MODEL.value}:
        return False

    status = payload.get("status")
    if status in {item.value for item in ResponseStatus}:
        return True

    if "response" in payload and set(payload).issubset({"response", "metadata", "protocol_version", "responded_at"}):
        return True
    if "output" in payload and set(payload).issubset({"output", "metadata", "protocol_version", "responded_at"}):
        return True
    if "error" in payload and set(payload).issubset({"error", "metadata", "protocol_version", "responded_at"}):
        return True
    return False


def _normalize_request_kind(value: InteractionKind | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, InteractionKind):
        return value.value
    return str(value)
