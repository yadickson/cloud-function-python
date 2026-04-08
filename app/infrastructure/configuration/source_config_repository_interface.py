from abc import abstractmethod
from typing import List

from app.infrastructure.configuration.connector_config_repository_interface import ConnectorConfigRepositoryInterface


class SourceConfigRepositoryInterface(ConnectorConfigRepositoryInterface):
    @abstractmethod
    def get_source_directory(self) -> str:
        pass

    @abstractmethod
    def get_source_full_filename(self, filename: str) -> str:
        pass

    @abstractmethod
    def get_source_file_filters(self) -> List[str]:
        pass
