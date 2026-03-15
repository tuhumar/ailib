from __future__ import annotations

from typing import Any

from .backends.base import Backend
from .models import InteractionKind, RequestEnvelope, ResponseEnvelope
from .parsing import extract_json_payload, model_schema, normalize_choice, validate_json_payload_schema, validate_model_instance


class Client:
    def __init__(self, backend: Backend):
        self.backend = backend

    def ask(self, prompt: str, context: Any = None, timeout_s: float | None = None, metadata: dict[str, Any] | None = None) -> str:
        response = self._send(
            kind=InteractionKind.ASK,
            prompt=prompt,
            context=context,
            timeout_s=timeout_s,
            metadata=metadata,
        )
        return response.output or ""

    def decide(
        self,
        prompt: str,
        options: list[str],
        context: Any = None,
        timeout_s: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        response = self._send(
            kind=InteractionKind.DECIDE,
            prompt=prompt,
            context=context,
            options=options,
            timeout_s=timeout_s,
            metadata=metadata,
        )
        return normalize_choice(response.output or "", options)

    def ask_json(
        self,
        prompt: str,
        context: Any = None,
        timeout_s: float | None = None,
        metadata: dict[str, Any] | None = None,
        schema: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[Any]:
        response = self._send(
            kind=InteractionKind.ASK_JSON,
            prompt=prompt,
            context=context,
            timeout_s=timeout_s,
            metadata=metadata,
            schema=schema,
        )
        payload = extract_json_payload(response.output or "")
        if schema is not None:
            validate_json_payload_schema(payload, schema)
        return payload

    def ask_model(
        self,
        prompt: str,
        model_cls: type,
        context: Any = None,
        timeout_s: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        try:
            import pydantic  # noqa: F401
        except ImportError as exc:
            raise ImportError("pydantic must be installed to use ask_model().") from exc

        schema = model_schema(model_cls)
        payload = self.ask_json(
            prompt=prompt,
            context=context,
            timeout_s=timeout_s,
            metadata=metadata,
            schema=schema,
        )
        if not isinstance(payload, dict):
            raise TypeError("ask_model() requires a JSON object response.")
        return validate_model_instance(model_cls, payload)

    def request(self, envelope: RequestEnvelope):
        return ResponseEnvelope.coerce(
            self.backend.send(envelope),
            fallback_request_id=envelope.request_id,
            request_kind=envelope.kind,
        )

    def _send(
        self,
        kind: InteractionKind,
        prompt: str,
        context: Any = None,
        options: list[str] | None = None,
        schema: dict[str, Any] | None = None,
        timeout_s: float | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        envelope = RequestEnvelope(
            prompt=prompt,
            kind=kind,
            context=context,
            options=options,
            schema=schema,
            timeout_s=timeout_s,
            metadata=dict(metadata or {}),
        )
        return self.request(envelope).require_ok()
