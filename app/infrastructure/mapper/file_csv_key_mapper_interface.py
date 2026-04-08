from abc import ABC, abstractmethod


class FileCsvKeyMapperInterface(ABC):
    @abstractmethod
    def get_key(self, line: bytes) -> str:
        pass
