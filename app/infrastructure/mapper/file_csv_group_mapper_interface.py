from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FileCsvGroupMapperInterface(ABC):
    @abstractmethod
    def group(self, file: FileModel) -> List[List[bytes]]:
        pass
