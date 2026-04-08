from abc import ABC, abstractmethod
from typing import List


class GetFilesGatewayInterface(ABC):
    @abstractmethod
    def get_files_from_sftp(self) -> List[str]:
        pass
