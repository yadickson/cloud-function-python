from abc import ABC, abstractmethod

from app.domain.model.file_model import FileModel


class FileCryptoMapperInterface(ABC):
    @abstractmethod
    def encode(self, file: FileModel) -> FileModel:
        pass
