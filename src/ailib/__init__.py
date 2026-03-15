from .backends import Backend, FileBackend, StdioBackend, StdinBackend
from .client import Client
from .context import get_client, reset_context, set_backend, set_client, use_backend
from .exceptions import (
    AILibError,
    AILibTimeoutError,
    ConfigurationError,
    InvalidChoiceError,
    InvalidJSONError,
    ProtocolError,
    RemoteExecutionError,
    SchemaValidationError,
    RequestCancelledError,
    TransportError,
)
from .host import (
    format_stdio_response,
    parse_stdio_request,
    read_file_request,
    read_stdio_request,
    write_file_response,
    write_file_response_cancelled,
    write_file_response_error,
    write_file_response_ok,
    write_stdio_response,
    write_stdio_response_cancelled,
    write_stdio_response_error,
    write_stdio_response_ok,
)
from .logging_utils import setup_logging
from .models import InteractionKind, PROTOCOL_VERSION, RequestEnvelope, ResponseEnvelope, ResponseStatus


def ask(prompt, context=None, timeout_s=None, metadata=None):
    return get_client().ask(prompt, context=context, timeout_s=timeout_s, metadata=metadata)


def decide(prompt, options, context=None, timeout_s=None, metadata=None):
    return get_client().decide(
        prompt,
        options=options,
        context=context,
        timeout_s=timeout_s,
        metadata=metadata,
    )


def ask_json(prompt, context=None, timeout_s=None, metadata=None, schema=None):
    return get_client().ask_json(
        prompt,
        context=context,
        timeout_s=timeout_s,
        metadata=metadata,
        schema=schema,
    )


def ask_model(prompt, model_cls, context=None, timeout_s=None, metadata=None):
    return get_client().ask_model(
        prompt,
        model_cls=model_cls,
        context=context,
        timeout_s=timeout_s,
        metadata=metadata,
    )


__all__ = [
    "AILibError",
    "AILibTimeoutError",
    "Backend",
    "Client",
    "ConfigurationError",
    "FileBackend",
    "InteractionKind",
    "InvalidChoiceError",
    "InvalidJSONError",
    "PROTOCOL_VERSION",
    "ProtocolError",
    "RemoteExecutionError",
    "SchemaValidationError",
    "RequestCancelledError",
    "RequestEnvelope",
    "ResponseEnvelope",
    "ResponseStatus",
    "StdioBackend",
    "StdinBackend",
    "TransportError",
    "ask",
    "ask_json",
    "ask_model",
    "decide",
    "format_stdio_response",
    "get_client",
    "parse_stdio_request",
    "read_file_request",
    "read_stdio_request",
    "reset_context",
    "set_backend",
    "set_client",
    "setup_logging",
    "use_backend",
    "write_file_response",
    "write_file_response_cancelled",
    "write_file_response_error",
    "write_file_response_ok",
    "write_stdio_response",
    "write_stdio_response_cancelled",
    "write_stdio_response_error",
    "write_stdio_response_ok",
]
