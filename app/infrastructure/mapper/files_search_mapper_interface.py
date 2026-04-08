from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FilesSearchMapperInterface(ABC):
    @abstractmethod
    def search(self, files: List[FileModel], search: list[str]) -> List[FileModel]:
        pass
