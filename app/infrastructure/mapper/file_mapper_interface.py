from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FileMapperInterface(ABC):
    @abstractmethod
    def get_files(self, file: FileModel) -> List[FileModel]:
        pass
