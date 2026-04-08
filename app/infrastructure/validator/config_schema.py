from marshmallow import Schema

from app.infrastructure.validator.optional_string_schema import optional_string_schema
from app.infrastructure.validator.required_integer_schema import required_integer_schema
from app.infrastructure.validator.required_string_schema import required_string_schema


class ConfigSchema(Schema):
    project_id = required_string_schema("PROJECT_ID")
    secret_id = required_string_schema("SECRET_ID")
    version_id = optional_string_schema("VERSION_ID")
    time_zone = optional_string_schema("TIME_ZONE")
    source_host = required_string_schema("SOURCE_HOST")
    source_port = required_integer_schema("SOURCE_PORT")
    source_username = required_string_schema("SOURCE_USERNAME")
    source_password = required_string_schema("SOURCE_PASSWORD")
    source_directory = required_string_schema("SOURCE_DIRECTORY")
    source_file_filters = required_string_schema("SOURCE_FILE_FILTERS")
    dest_host = required_string_schema("DEST_HOST")
    dest_port = required_integer_schema("DEST_PORT")
    dest_username = required_string_schema("DEST_USERNAME")
    dest_password = required_string_schema("DEST_PASSWORD")
    dest_directory = required_string_schema("DEST_DIRECTORY")
    dest_file_max_registers = required_integer_schema("DEST_FILE_MAX_REGISTERS")
    pgp_public_key = required_string_schema("PGP_PUBLIC_KEY")
    pgp_private_key = optional_string_schema("PGP_PRIVATE_KEY")
    pgp_password = optional_string_schema("PGP_PASSWORD")
