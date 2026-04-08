from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_mapper_interface import FileMapperInterface
from app.infrastructure.mapper.file_zip_raw_reader_mapper_interface import FileZipRawReaderMapperInterface
from app.infrastructure.mapper.file_zip_reader_mapper_interface import FileZipReaderMapperInterface
from app.infrastructure.mapper.files_group_mapper_interface import FilesGroupMapperInterface


class FileMapper(FileMapperInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        file_zip_reader_mapper: FileZipReaderMapperInterface,
        file_zip_raw_reader_mapper: FileZipRawReaderMapperInterface,
        files_group_mapper: FilesGroupMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.file_zip_reader_mapper = file_zip_reader_mapper
        self.file_zip_raw_reader_mapper = file_zip_raw_reader_mapper
        self.files_group_mapper = files_group_mapper

    def get_files(self, file: FileModel) -> List[FileModel]:
        try:
            files = self.file_zip_reader_mapper.read(file=file)
        except Exception as exception:
            self.logger_repository.error(message="Try to read corrupted file.", cause=exception)
            files = self.file_zip_raw_reader_mapper.read(file=file)

        return self.files_group_mapper.group(file=file, files=files)
