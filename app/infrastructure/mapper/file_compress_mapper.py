import io
import zipfile
from typing import List

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_compress_mapper_interface import FileCompressMapperInterface


class FileCompressMapper(FileCompressMapperInterface):
    def compress(self, filename: str, files: List[FileModel]) -> FileModel:
        with io.BytesIO() as buffer:
            with zipfile.ZipFile(buffer, mode="w") as zip_file:
                for file in files:
                    zip_file.writestr(file.filename, file.content)
            return FileModel(filename, buffer.getvalue())
