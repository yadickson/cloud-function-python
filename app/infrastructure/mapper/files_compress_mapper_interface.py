from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FilesCompressMapperInterface(ABC):
    @abstractmethod
    def compress(self, file: FileModel, csv_file: FileModel, files: List[FileModel]) -> FileModel:
        pass
