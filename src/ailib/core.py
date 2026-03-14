from typing import Any, List, Optional, TypeVar, Union, Dict, Iterator
import json
import os
from contextlib import contextmanager
from .backends import Backend, StdinBackend, FileBackend

T = TypeVar('T')

class Context:
    """Singleton context to manage the global ailib backend."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Context, cls).__new__(cls)
            cls._instance.backend = cls._initialize_default_backend()
        return cls._instance
    
    @staticmethod
    def _initialize_default_backend() -> Backend:
        """Initialize backend based on environment variables."""
        env_backend = os.getenv("AILIB_BACKEND", "stdin").lower()
        if env_backend == "file":
            return FileBackend()
        return StdinBackend()
    
    def set_backend(self, backend: Backend):
        self.backend = backend

_context = Context()

def set_backend(backend: Backend) -> None:
    """Set the global communication backend for ailib."""
    _context.set_backend(backend)

@contextmanager
def use_backend(backend: Backend) -> Iterator[None]:
    """Temporarily switch backend within a 'with' block."""
    old_backend = _context.backend
    _context.set_backend(backend)
    try:
        yield
    finally:
        _context.set_backend(old_backend)

def ask(prompt: str, context: Optional[Any] = None) -> str:
    """Request a free-text response from the AI agent."""
    return _context.backend.request(prompt=prompt, context=context)

def ask_json(prompt: str, context: Optional[Any] = None) -> Union[Dict[str, Any], List[Any]]:
    """Request and parse a JSON response from the AI agent."""
    response = _context.backend.request(prompt=prompt, context=context)
    
    clean_response = response.strip()
    
    # Try to extract JSON from markdown code blocks or free text
    if "```json" in clean_response:
        clean_response = clean_response.split("```json")[1].split("```")[0].strip()
    elif "```" in clean_response:
        clean_response = clean_response.split("```")[1].split("```")[0].strip()
    elif "{" in clean_response and "}" in clean_response:
        start = clean_response.find("{")
        end = clean_response.rfind("}") + 1
        clean_response = clean_response[start:end]

    try:
        return json.loads(clean_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON format: {response}") from e

def decide(prompt: str, options: List[str], context: Optional[Any] = None) -> str:
    """Request the AI to choose one from a list of options."""
    return _context.backend.request(prompt=prompt, options=options, context=context)
