from abc import ABC, abstractmethod


class DelFileGatewayInterface(ABC):
    @abstractmethod
    def del_file_from_sftp(self, filename: str) -> None:
        pass
