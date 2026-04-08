from abc import ABC, abstractmethod

from app.domain.model.file_model import FileModel


class GetFileGatewayInterface(ABC):
    @abstractmethod
    def get_file_from_sftp(self, filename: str) -> FileModel:
        pass
