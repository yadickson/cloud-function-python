from abc import ABC, abstractmethod


class FileZipInfoMapperInterface(ABC):
    @abstractmethod
    def get_decompress_size(self, content: bytes) -> int:
        pass

    @abstractmethod
    def get_filename_size(self, content: bytes) -> int:
        pass

    @abstractmethod
    def get_filename(self, content: bytes) -> str:
        pass

    @abstractmethod
    def get_body(self, content: bytes) -> bytes:
        pass
