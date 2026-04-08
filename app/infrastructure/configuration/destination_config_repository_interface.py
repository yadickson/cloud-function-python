from abc import abstractmethod

from app.infrastructure.configuration.connector_config_repository_interface import ConnectorConfigRepositoryInterface


class DestinationConfigRepositoryInterface(ConnectorConfigRepositoryInterface):
    @abstractmethod
    def get_destination_directory(self) -> str:
        pass

    @abstractmethod
    def get_destination_full_filename(self, filename: str) -> str:
        pass

    @abstractmethod
    def get_destination_file_max_registers(self) -> int:
        pass
