from __future__ import annotations

import os
from contextlib import contextmanager

from .backends import FileBackend, StdioBackend
from .client import Client
from .exceptions import ConfigurationError


def build_backend_from_env():
    backend_name = os.getenv("AILIB_BACKEND", "stdio").lower()
    timeout_s = float(os.getenv("AILIB_TIMEOUT", "300"))

    if backend_name in {"stdio", "stdin"}:
        return StdioBackend(default_timeout=timeout_s)
    if backend_name == "file":
        return FileBackend(default_timeout=timeout_s)
    raise ConfigurationError(f"Unsupported AILIB_BACKEND value: {backend_name}")


class Context:
    def __init__(self):
        self.client: Client | None = None

    def get_client(self) -> Client:
        if self.client is None:
            self.client = Client(build_backend_from_env())
        return self.client

    def set_client(self, client: Client) -> None:
        self.client = client

    def set_backend(self, backend) -> None:
        self.client = Client(backend)

    def reset(self, client: Client | None = None) -> None:
        self.client = client


_context = Context()


def get_client() -> Client:
    return _context.get_client()


def set_client(client: Client) -> None:
    _context.set_client(client)


def set_backend(backend) -> None:
    _context.set_backend(backend)


def reset_context(client: Client | None = None) -> None:
    _context.reset(client)


@contextmanager
def use_backend(backend):
    old_client = _context.client
    _context.set_backend(backend)
    try:
        yield
    finally:
        _context.reset(old_client)
