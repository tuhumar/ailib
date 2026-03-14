import unittest
from unittest.mock import MagicMock
import sys
import os
import json

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import ailib
from ailib.backends import Backend

class MockBackend(Backend):
    def request(self, prompt, context=None, options=None):
        return f"Response to: {prompt}"

class TestAilib(unittest.TestCase):
    def test_ask(self):
        mock = MockBackend()
        ailib.set_backend(mock)
        
        result = ailib.ask("Hello")
        self.assertEqual(result, "Response to: Hello")

    def test_ask_json(self):
        mock = MagicMock()
        mock.request.return_value = '{"status": "ok", "value": 42}'
        ailib.set_backend(mock)
        
        result = ailib.ask_json("Give me JSON")
        self.assertEqual(result, {"status": "ok", "value": 42})

    def test_stdin_backend_output(self):
        """Verify that StdinBackend prints the expected markers to stderr."""
        backend = ailib.StdinBackend()
        
        # Mock input to avoid blocking
        import builtins
        original_input = builtins.input
        builtins.input = lambda _: "AI response"
        
        from io import StringIO
        saved_stderr = sys.stderr
        try:
            err = StringIO()
            sys.stderr = err
            result = backend.request("Test prompt", context={"key": "val"})
            self.assertEqual(result, "AI response")
            
            output = err.getvalue()
            self.assertIn("<<<AILIB_REQUEST_START>>>", output)
            self.assertIn("Test prompt", output)
            self.assertIn("key", output)
            self.assertIn("<<<AILIB_REQUEST_END>>>", output)
        finally:
            sys.stderr = saved_stderr
            builtins.input = original_input

if __name__ == '__main__':
    unittest.main()
