from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FilesGroupMapperInterface(ABC):
    @abstractmethod
    def group(self, file: FileModel, files: List[FileModel]) -> List[FileModel]:
        pass
