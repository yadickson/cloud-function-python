from abc import ABC, abstractmethod
from typing import Optional


class LoggerRepositoryInterface(ABC):
    @abstractmethod
    def running(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass

    @abstractmethod
    def warn(self, message: str, cause: Optional[Exception] = None) -> None:
        pass

    @abstractmethod
    def error(self, message: str, cause: Optional[Exception] = None) -> None:
        pass

    @abstractmethod
    def success(self, message: str) -> None:
        pass
