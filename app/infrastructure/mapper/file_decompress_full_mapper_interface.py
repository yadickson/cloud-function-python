from abc import ABC, abstractmethod

from app.domain.model.file_model import FileModel


class FileDecompressFullMapperInterface(ABC):
    @abstractmethod
    def decompress_full(self, content: bytes) -> FileModel:
        pass
