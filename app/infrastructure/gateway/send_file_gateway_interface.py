from abc import ABC, abstractmethod

from app.domain.model.file_model import FileModel


class SendFileGatewayInterface(ABC):
    @abstractmethod
    def send_file_to_sftp(self, file: FileModel) -> None:
        pass
