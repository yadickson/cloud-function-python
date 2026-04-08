from abc import ABC, abstractmethod


class LoggerExtrasInterface(ABC):
    @abstractmethod
    def get_extras(self) -> dict[str, str]:
        pass
