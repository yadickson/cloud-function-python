from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FileCsvSplitMapperInterface(ABC):
    @abstractmethod
    def split(self, file: FileModel) -> List[FileModel]:
        pass
