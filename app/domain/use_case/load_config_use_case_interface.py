from abc import ABC, abstractmethod


class LoadConfigUseCaseInterface(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
