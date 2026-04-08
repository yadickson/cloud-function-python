from dataclasses import dataclass


@dataclass
class ConfigModel:
    project_id: str
    secret_id: str
    version_id: str
    time_zone: str
    source_host: str
    source_port: str
    source_username: str
    source_password: str
    source_directory: str
    source_file_filters: str
    dest_host: str
    dest_port: str
    dest_username: str
    dest_password: str
    dest_directory: str
    dest_file_max_registers: str
    pgp_public_key: str
    pgp_private_key: str
    pgp_password: str
