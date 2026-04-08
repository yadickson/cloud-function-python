from abc import ABC, abstractmethod


class Base64SecurityInterface(ABC):
    @abstractmethod
    def encode(self, content: str) -> str:
        pass

    @abstractmethod
    def decode(self, content: str) -> str:
        pass
