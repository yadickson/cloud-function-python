from abc import ABC, abstractmethod


class ConnectorConfigRepositoryInterface(ABC):
    @abstractmethod
    def get_host(self) -> str:
        pass

    @abstractmethod
    def get_port(self) -> int:
        pass

    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass
