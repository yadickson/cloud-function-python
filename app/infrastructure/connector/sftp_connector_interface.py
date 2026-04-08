from abc import ABC, abstractmethod

from pysftp import Connection

from app.infrastructure.configuration.connector_config_repository_interface import ConnectorConfigRepositoryInterface


class SftpConnectorInterface(ABC):
    @abstractmethod
    def get_connection(self, config: ConnectorConfigRepositoryInterface) -> Connection:
        pass
