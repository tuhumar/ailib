class AILibError(Exception):
    """Base exception for the library."""


class ConfigurationError(AILibError):
    """Raised when the library is misconfigured."""


class ProtocolError(AILibError):
    """Raised when a request or response payload is malformed."""


class TransportError(AILibError):
    """Raised when the transport cannot complete the exchange."""


class AILibTimeoutError(TransportError):
    """Raised when the supervising agent does not answer in time."""


class RequestCancelledError(AILibError):
    """Raised when the supervising agent explicitly cancels the request."""


class RemoteExecutionError(AILibError):
    """Raised when the supervising agent answers with an error."""


class InvalidChoiceError(AILibError):
    """Raised when a decision response is not one of the allowed options."""


class InvalidJSONError(AILibError):
    """Raised when the response cannot be parsed as JSON."""


class SchemaValidationError(AILibError):
    """Raised when a JSON payload does not satisfy the expected schema."""
