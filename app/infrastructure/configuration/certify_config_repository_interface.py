from abc import ABC, abstractmethod


class CertifyConfigRepositoryInterface(ABC):
    @abstractmethod
    def get_public_key(self) -> str:
        pass

    @abstractmethod
    def get_private_key(self) -> str:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass
