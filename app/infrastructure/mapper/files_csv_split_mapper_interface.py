from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FilesCsvSplitMapperInterface(ABC):
    @abstractmethod
    def split(self, files: List[FileModel]) -> List[FileModel]:
        pass
