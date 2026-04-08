import os

from injector import inject

from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.destination_config_repository_interface import DestinationConfigRepositoryInterface
from app.infrastructure.security.base64_security_interface import Base64SecurityInterface


class DestinationConfigRepository(DestinationConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        config_repository: ConfigRepositoryInterface,
        base64_security: Base64SecurityInterface,
    ) -> None:
        self.config_repository = config_repository
        self.base64_security = base64_security

    def get_host(self) -> str:
        return self.config_repository.get_configuration().dest_host

    def get_port(self) -> int:
        return int(self.config_repository.get_configuration().dest_port)

    def get_username(self) -> str:
        return self.config_repository.get_configuration().dest_username

    def get_password(self) -> str:
        return self.base64_security.decode(self.config_repository.get_configuration().dest_password)

    def get_destination_directory(self) -> str:
        return self.config_repository.get_configuration().dest_directory

    def get_destination_full_filename(self, filename: str) -> str:
        return os.path.join(self.get_destination_directory(), filename)

    def get_destination_file_max_registers(self) -> int:
        return int(self.config_repository.get_configuration().dest_file_max_registers)
