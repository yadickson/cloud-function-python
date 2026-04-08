from typing import Any

from marshmallow import fields


def required_integer_schema(field_name: str) -> Any:
    return fields.Integer(
        required=True,
        error_messages={"required": f"{field_name} is required.", "null": f"{field_name} is required.", "invalid": f"{field_name} is required."},
    )
