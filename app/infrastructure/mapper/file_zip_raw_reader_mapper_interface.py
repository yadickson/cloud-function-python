from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class FileZipRawReaderMapperInterface(ABC):
    @abstractmethod
    def read(self, file: FileModel) -> List[FileModel]:
        pass
