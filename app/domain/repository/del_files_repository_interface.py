from abc import ABC, abstractmethod


class DelFilesRepositoryInterface(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
