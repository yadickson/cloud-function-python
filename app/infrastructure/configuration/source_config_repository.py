import os
from typing import List

from injector import inject

from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface


class SourceConfigRepository(SourceConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        config_repository: ConfigRepositoryInterface,
    ) -> None:
        self.config_repository = config_repository

    def get_host(self) -> str:
        return self.config_repository.get_configuration().source_host

    def get_port(self) -> int:
        return int(self.config_repository.get_configuration().source_port)

    def get_username(self) -> str:
        return self.config_repository.get_configuration().source_username

    def get_password(self) -> str:
        return self.config_repository.get_configuration().source_password

    def get_source_directory(self) -> str:
        return self.config_repository.get_configuration().source_directory

    def get_source_full_filename(self, filename: str) -> str:
        return os.path.join(self.get_source_directory(), filename)

    def get_source_file_filters(self) -> List[str]:
        file_filters = self.config_repository.get_configuration().source_file_filters
        return [file for file in file_filters.split("|")]
