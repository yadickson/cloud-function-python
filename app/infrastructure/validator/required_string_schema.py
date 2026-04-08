from typing import Any

from marshmallow import fields, validate


def required_string_schema(field_name: str) -> Any:
    return fields.String(
        required=True,
        validate=validate.Length(min=1, error=f"{field_name} is required."),
        error_messages={"required": f"{field_name} is required.", "null": f"{field_name} is required."},
    )
