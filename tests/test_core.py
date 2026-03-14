import pytest
from unittest.mock import MagicMock
import ailib
from ailib.backends import Backend

class MockBackend(Backend):
    def request(self, prompt, context=None, options=None):
        return f"Response to: {prompt}"

def test_ask():
    mock = MockBackend()
    ailib.set_backend(mock)
    
    result = ailib.ask("Hello")
    assert result == "Response to: Hello"

def test_decide():
    mock = MockBackend()
    ailib.set_backend(mock)
    
    result = ailib.decide("Choose", options=["A", "B"])
    assert result == "Response to: Choose"

def test_stdin_backend_output(capsys):
    """Verify that StdinBackend prints the expected markers."""
    backend = ailib.StdinBackend()
    
    # Mock input to avoid blocking
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: "AI response"
    
    try:
        result = backend.request("Test prompt", context={"key": "val"})
        assert result == "AI response"
        
        captured = capsys.readouterr()
        assert "<<<AILIB_REQUEST_START>>>" in captured.out
        assert "Test prompt" in captured.out
        assert "key" in captured.out
        assert "<<<AILIB_REQUEST_END>>>" in captured.out
    finally:
        builtins.input = original_input
