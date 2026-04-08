from abc import ABC, abstractmethod

from pysftp import CnOpts


class SftpConnectorOptionsInterface(ABC):
    @abstractmethod
    def get_options(self) -> CnOpts:
        pass
