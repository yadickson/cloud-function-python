from abc import ABC, abstractmethod
from typing import List


class FilesFiltersMapperInterface(ABC):
    @abstractmethod
    def get_files(self) -> List[str]:
        pass
