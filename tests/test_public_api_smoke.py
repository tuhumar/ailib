import unittest

import ailib
from ailib.exceptions import RequestCancelledError, RemoteExecutionError
from ailib.models import InteractionKind, RequestEnvelope, ResponseEnvelope, ResponseStatus


class DummyBackend:
    def send(self, envelope):
        if envelope.kind == InteractionKind.ASK:
            return ResponseEnvelope(request_id=envelope.request_id, output=f"Response to: {envelope.prompt}")
        if envelope.kind == InteractionKind.DECIDE:
            return ResponseEnvelope(request_id=envelope.request_id, output="A")
        if envelope.kind == InteractionKind.ASK_JSON:
            return ResponseEnvelope(request_id=envelope.request_id, output='{"status": "ok", "value": 42}')
        if envelope.kind == InteractionKind.ASK_MODEL:
            return ResponseEnvelope(request_id=envelope.request_id, output='{"action": "retry", "eta_minutes": 5}')
        return ResponseEnvelope(request_id=envelope.request_id, status=ResponseStatus.ERROR, error="unsupported")


class PublicApiSmokeTests(unittest.TestCase):
    def setUp(self):
        ailib.reset_context()
        ailib.set_backend(DummyBackend())

    def tearDown(self):
        ailib.reset_context()

    def test_ask(self):
        result = ailib.ask("Hello")
        self.assertEqual(result, "Response to: Hello")

    def test_decide(self):
        result = ailib.decide("Choose", options=["A", "B"])
        self.assertEqual(result, "A")

    def test_ask_json(self):
        result = ailib.ask_json("Give me JSON")
        self.assertEqual(result, {"status": "ok", "value": 42})

    def test_request_envelope_roundtrip(self):
        envelope = RequestEnvelope(prompt="Hello", kind=InteractionKind.ASK, metadata={"x": 1})
        cloned = RequestEnvelope.from_dict(envelope.to_dict())
        self.assertEqual(cloned.prompt, "Hello")
        self.assertEqual(cloned.kind, InteractionKind.ASK)
        self.assertEqual(cloned.metadata, {"x": 1})
        self.assertEqual(cloned.request_id, envelope.request_id)

    def test_response_envelope_require_ok_error(self):
        response = ResponseEnvelope(request_id="r1", status=ResponseStatus.ERROR, error="boom")
        with self.assertRaises(RemoteExecutionError):
            response.require_ok()

    def test_response_envelope_require_ok_cancelled(self):
        response = ResponseEnvelope(request_id="r1", status=ResponseStatus.CANCELLED, error="cancelled")
        with self.assertRaises(RequestCancelledError):
            response.require_ok()


if __name__ == "__main__":
    unittest.main()
