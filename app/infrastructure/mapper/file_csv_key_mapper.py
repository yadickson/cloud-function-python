from app.infrastructure.constants.encodings_enum import EncodingsEnum
from app.infrastructure.mapper.file_csv_key_mapper_interface import FileCsvKeyMapperInterface


class FileCsvKeyMapper(FileCsvKeyMapperInterface):
    def get_key(self, line: bytes) -> str:
        return line.decode(EncodingsEnum.UTF8).split(";")[1].split("-")[0].replace(".", "")
