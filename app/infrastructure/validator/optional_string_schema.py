from typing import Any

from marshmallow import fields


def optional_string_schema(field_name: str) -> Any:
    return fields.String(allow_none=True, error_messages={"invalid": f"{field_name} is not ok."})
