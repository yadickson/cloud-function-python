from abc import ABC, abstractmethod


class TransferFilesUseCaseInterface(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
