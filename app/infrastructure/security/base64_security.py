import base64

from app.infrastructure.constants.encodings_enum import EncodingsEnum
from app.infrastructure.security.base64_security_interface import Base64SecurityInterface


class Base64Security(Base64SecurityInterface):
    def encode(self, content: str) -> str:
        return base64.b64encode(content.encode(EncodingsEnum.ASCII)).decode(EncodingsEnum.ASCII)

    def decode(self, content: str) -> str:
        return base64.b64decode(content.encode(EncodingsEnum.ASCII)).decode(EncodingsEnum.ASCII)
