from abc import ABC, abstractmethod
from typing import List


class FilesFilteredMapperInterface(ABC):
    @abstractmethod
    def filter(self, files: List[str]) -> List[str]:
        pass
