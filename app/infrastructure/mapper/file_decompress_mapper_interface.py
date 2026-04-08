from abc import ABC, abstractmethod

from app.domain.model.file_model import FileModel


class FileDecompressMapperInterface(ABC):
    @abstractmethod
    def decompress(self, content: bytes) -> FileModel:
        pass
