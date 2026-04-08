from app.infrastructure.constants.encodings_enum import EncodingsEnum
from app.infrastructure.mapper.file_zip_info_mapper_interface import FileZipInfoMapperInterface


class FileZipInfoMapper(FileZipInfoMapperInterface):
    def get_decompress_size(self, content: bytes) -> int:
        return int(bytearray([content[21], content[20], content[23], content[22]]).hex(), 16)  # pragma: no mutate

    def get_filename_size(self, content: bytes) -> int:
        return int(content[25:27].hex(), 16)  # pragma: no mutate

    def get_filename(self, content: bytes) -> str:
        filename_size = self.get_filename_size(content)
        return content[30 : filename_size + 30].decode(EncodingsEnum.ASCII)  # pragma: no mutate

    def get_body(self, content: bytes) -> bytes:
        filename_size = self.get_filename_size(content)
        return content[30 + filename_size :]  # pragma: no mutate
