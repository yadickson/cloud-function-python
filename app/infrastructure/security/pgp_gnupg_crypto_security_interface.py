from abc import ABC, abstractmethod


class PgpGnuPgCryptoSecurityInterface(ABC):
    @abstractmethod
    def encode(self, content: bytes) -> bytes:
        pass

    @abstractmethod
    def decode(self, content: bytes) -> bytes:
        pass
