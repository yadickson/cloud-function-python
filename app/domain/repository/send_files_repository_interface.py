from abc import ABC, abstractmethod
from typing import List

from app.domain.model.file_model import FileModel


class SendFilesRepositoryInterface(ABC):
    @abstractmethod
    def execute(self, files: List[FileModel]) -> None:
        pass
