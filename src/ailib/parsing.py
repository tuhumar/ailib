from __future__ import annotations

import json
import re
from typing import Any

from .exceptions import InvalidChoiceError, InvalidJSONError, SchemaValidationError


def extract_json_payload(text: str) -> dict[str, Any] | list[Any]:
    clean = text.strip()
    markdown_match = re.search(r"```(?:json)?\s*(.*?)\s*```", clean, re.IGNORECASE | re.DOTALL)
    if markdown_match:
        clean = markdown_match.group(1).strip()
    else:
        clean = _extract_bracket_payload(clean)
    try:
        parsed = json.loads(clean)
    except json.JSONDecodeError as exc:
        raise InvalidJSONError(f"Invalid JSON payload: {exc}. Raw response: {text}") from exc
    if not isinstance(parsed, (dict, list)):
        raise InvalidJSONError("JSON payload must decode to an object or an array.")
    return parsed


def validate_json_payload_schema(payload: dict[str, Any] | list[Any], schema: dict[str, Any]) -> None:
    if not isinstance(schema, dict):
        raise TypeError("schema must be a dictionary.")

    try:
        import jsonschema
    except ImportError:
        _validate_schema_subset(payload, schema, path="$")
        return

    try:
        jsonschema.validate(payload, schema)
    except jsonschema.exceptions.ValidationError as exc:
        path = "$"
        if exc.path:
            path = "$"
            for item in exc.path:
                path = f"{path}[{item}]" if isinstance(item, int) else f"{path}.{item}"
        message = exc.message or "Payload does not satisfy the provided schema."
        raise SchemaValidationError(f"Schema validation failed at {path}: {message}") from exc


def normalize_choice(value: str, options: list[str]) -> str:
    candidate = value.strip()
    if candidate in options:
        return candidate

    lower_map = {option.lower(): option for option in options}
    lowered = candidate.lower()
    if lowered in lower_map:
        return lower_map[lowered]

    if candidate.isdigit():
        index = int(candidate)
        if 0 <= index < len(options):
            return options[index]

    bracket_match = re.fullmatch(r"\[(\d+)\]", candidate)
    if bracket_match:
        index = int(bracket_match.group(1))
        if 0 <= index < len(options):
            return options[index]

    raise InvalidChoiceError(f"Agent returned '{value}', but allowed options are: {options}")


def model_schema(model_cls: type) -> dict[str, Any]:
    if hasattr(model_cls, "model_json_schema"):
        return model_cls.model_json_schema()
    if hasattr(model_cls, "schema"):
        return model_cls.schema()
    raise TypeError("The provided model class does not expose a Pydantic schema method.")


def validate_model_instance(model_cls: type, data: dict[str, Any] | list[Any]) -> Any:
    if hasattr(model_cls, "model_validate"):
        return model_cls.model_validate(data)
    if hasattr(model_cls, "parse_obj"):
        return model_cls.parse_obj(data)
    raise TypeError("The provided model class does not expose a Pydantic validation method.")


def _validate_schema_subset(payload: Any, schema: dict[str, Any], path: str) -> None:
    expected_type = schema.get("type")
    if expected_type is not None:
        type_names = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_matches_schema_type(payload, item) for item in type_names):
            joined = ", ".join(str(item) for item in type_names)
            raise SchemaValidationError(f"Schema validation failed at {path}: expected type {joined}.")

    if "const" in schema and payload != schema["const"]:
        raise SchemaValidationError(f"Schema validation failed at {path}: expected constant value {schema['const']!r}.")

    if "enum" in schema and payload not in schema["enum"]:
        raise SchemaValidationError(f"Schema validation failed at {path}: value {payload!r} is not in enum {schema['enum']!r}.")

    if isinstance(payload, dict):
        _validate_object_schema_subset(payload, schema, path)
    elif isinstance(payload, list):
        _validate_array_schema_subset(payload, schema, path)
    elif isinstance(payload, str):
        _validate_string_schema_subset(payload, schema, path)
    elif isinstance(payload, (int, float)) and not isinstance(payload, bool):
        _validate_numeric_schema_subset(payload, schema, path)


def _validate_object_schema_subset(payload: dict[str, Any], schema: dict[str, Any], path: str) -> None:
    properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    required = schema.get("required") if isinstance(schema.get("required"), list) else []
    additional_properties = schema.get("additionalProperties", True)

    for key in required:
        if key not in payload:
            raise SchemaValidationError(f"Schema validation failed at {path}: missing required property {key!r}.")

    for key, value in payload.items():
        next_path = f"{path}.{key}"
        if key in properties and isinstance(properties.get(key), dict):
            _validate_schema_subset(value, properties[key], next_path)
            continue
        if additional_properties is False:
            raise SchemaValidationError(f"Schema validation failed at {path}: unexpected property {key!r}.")
        if isinstance(additional_properties, dict):
            _validate_schema_subset(value, additional_properties, next_path)


def _validate_array_schema_subset(payload: list[Any], schema: dict[str, Any], path: str) -> None:
    min_items = schema.get("minItems")
    max_items = schema.get("maxItems")
    if min_items is not None and len(payload) < int(min_items):
        raise SchemaValidationError(f"Schema validation failed at {path}: expected at least {min_items} items.")
    if max_items is not None and len(payload) > int(max_items):
        raise SchemaValidationError(f"Schema validation failed at {path}: expected at most {max_items} items.")

    items = schema.get("items")
    if isinstance(items, dict):
        for index, item in enumerate(payload):
            _validate_schema_subset(item, items, f"{path}[{index}]")
    elif isinstance(items, list):
        for index, item_schema in enumerate(items):
            if index >= len(payload):
                break
            if isinstance(item_schema, dict):
                _validate_schema_subset(payload[index], item_schema, f"{path}[{index}]")


def _validate_string_schema_subset(payload: str, schema: dict[str, Any], path: str) -> None:
    min_length = schema.get("minLength")
    max_length = schema.get("maxLength")
    pattern = schema.get("pattern")

    if min_length is not None and len(payload) < int(min_length):
        raise SchemaValidationError(f"Schema validation failed at {path}: expected at least {min_length} characters.")
    if max_length is not None and len(payload) > int(max_length):
        raise SchemaValidationError(f"Schema validation failed at {path}: expected at most {max_length} characters.")
    if pattern and not re.search(str(pattern), payload):
        raise SchemaValidationError(f"Schema validation failed at {path}: string does not match pattern {pattern!r}.")


def _validate_numeric_schema_subset(payload: int | float, schema: dict[str, Any], path: str) -> None:
    minimum = schema.get("minimum")
    maximum = schema.get("maximum")

    if minimum is not None and payload < minimum:
        raise SchemaValidationError(f"Schema validation failed at {path}: expected a value >= {minimum}.")
    if maximum is not None and payload > maximum:
        raise SchemaValidationError(f"Schema validation failed at {path}: expected a value <= {maximum}.")


def _matches_schema_type(payload: Any, type_name: Any) -> bool:
    if type_name == "object":
        return isinstance(payload, dict)
    if type_name == "array":
        return isinstance(payload, list)
    if type_name == "string":
        return isinstance(payload, str)
    if type_name == "integer":
        return isinstance(payload, int) and not isinstance(payload, bool)
    if type_name == "number":
        return isinstance(payload, (int, float)) and not isinstance(payload, bool)
    if type_name == "boolean":
        return isinstance(payload, bool)
    if type_name == "null":
        return payload is None
    return True


def _extract_bracket_payload(text: str) -> str:
    start_object = text.find("{")
    end_object = text.rfind("}")
    start_list = text.find("[")
    end_list = text.rfind("]")

    if start_object != -1 and end_object != -1 and (start_list == -1 or start_object < start_list):
        return text[start_object : end_object + 1]
    if start_list != -1 and end_list != -1:
        return text[start_list : end_list + 1]
    return text
