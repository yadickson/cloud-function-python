from abc import ABC, abstractmethod

from app.domain.model.file_model import FileModel


class FileDecompressRawMapperInterface(ABC):
    @abstractmethod
    def decompress_raw(self, content: bytes) -> FileModel:
        pass
