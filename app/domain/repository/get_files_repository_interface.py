from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class GetFilesRepositoryInterface(ABC):
    @abstractmethod
    def execute(self) -> List[FileModel]:
        pass
