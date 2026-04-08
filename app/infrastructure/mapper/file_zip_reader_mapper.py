import io
import zipfile
from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_zip_reader_mapper_interface import FileZipReaderMapperInterface


class FileZipReaderMapper(FileZipReaderMapperInterface):
    @inject
    def __init__(self, logger_repository: LoggerRepositoryInterface) -> None:
        self.logger_repository = logger_repository

    def read(self, file: FileModel) -> List[FileModel]:
        self.logger_repository.info(message=f"Reading {file.filename} file.")

        files = []

        with io.BytesIO(file.content) as buffer:
            with zipfile.ZipFile(buffer) as zip_file:
                for filename in zip_file.namelist():
                    with zip_file.open(filename) as file_pointer:
                        files.append(FileModel(filename=filename, content=file_pointer.read()))

        self.logger_repository.info(message=f"Found {len(files)} files.")

        return files
