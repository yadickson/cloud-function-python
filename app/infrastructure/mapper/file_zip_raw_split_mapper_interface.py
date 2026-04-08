from abc import ABC, abstractmethod
from typing import List


class FileZipRawSplitMapperInterface(ABC):
    @abstractmethod
    def get_parts(self, content: bytes) -> List[bytes]:
        pass
