from abc import ABC, abstractmethod


class SecretConfigRepositoryInterface(ABC):
    @abstractmethod
    def get_secret_id(self) -> str:
        pass
