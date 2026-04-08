from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FileCompressMapperInterface(ABC):
    @abstractmethod
    def compress(self, filename: str, files: List[FileModel]) -> FileModel:
        pass
