import io
import json
import os
import tempfile
import unittest

import ailib
from pydantic import BaseModel

from ailib.host import parse_stdio_request, read_file_request, write_file_response_ok, write_stdio_response_ok
from ailib.models import InteractionKind, RequestEnvelope, ResponseEnvelope


class DummyModelBackend:
    def send(self, envelope):
        if envelope.kind == InteractionKind.ASK_JSON:
            return ResponseEnvelope(request_id=envelope.request_id, output='{"action": "retry", "eta_minutes": 5}')
        return ResponseEnvelope(request_id=envelope.request_id, output="ok")


class Plan(BaseModel):
    action: str
    eta_minutes: int


class HostHelpersSmokeTests(unittest.TestCase):
    def setUp(self):
        ailib.reset_context()

    def tearDown(self):
        ailib.reset_context()

    def test_ask_model(self):
        ailib.set_backend(DummyModelBackend())
        plan = ailib.ask_model("Plan next step", Plan)
        self.assertEqual(plan.action, "retry")
        self.assertEqual(plan.eta_minutes, 5)

    def test_parse_stdio_request(self):
        envelope = RequestEnvelope(prompt="Hello", kind=InteractionKind.ASK, metadata={"x": 1})
        text = "<<<AILIB_REQUEST_START>>>\n" + json.dumps(envelope.to_dict()) + "\n<<<AILIB_REQUEST_END>>>\n"
        parsed = parse_stdio_request(text)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.request_id, envelope.request_id)
        self.assertEqual(parsed.prompt, "Hello")

    def test_write_stdio_response_ok(self):
        buf = io.StringIO()
        write_stdio_response_ok("req1", "approved", stream=buf)
        rendered = buf.getvalue()
        self.assertIn("<<<AILIB_RESPONSE_START>>>", rendered)
        self.assertIn("approved", rendered)
        self.assertIn("<<<AILIB_RESPONSE_END>>>", rendered)

    def test_file_helpers(self):
        request = RequestEnvelope(prompt="Hello", kind=InteractionKind.ASK)
        with tempfile.TemporaryDirectory() as tmpdir:
            request_path = os.path.join(tmpdir, "request.json")
            response_path = os.path.join(tmpdir, "response.json")

            with open(request_path, "w", encoding="utf-8") as handle:
                json.dump(request.to_dict(), handle)

            parsed_request = read_file_request(request_path)
            self.assertIsNotNone(parsed_request)
            self.assertEqual(parsed_request.request_id, request.request_id)

            write_file_response_ok(response_path, request.request_id, "approved")
            with open(response_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)

            self.assertEqual(payload["request_id"], request.request_id)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["output"], "approved")


if __name__ == "__main__":
    unittest.main()
