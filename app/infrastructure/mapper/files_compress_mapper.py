from pathlib import Path
from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_compress_mapper_interface import FileCompressMapperInterface
from app.infrastructure.mapper.files_compress_mapper_interface import FilesCompressMapperInterface
from app.infrastructure.mapper.files_search_mapper_interface import FilesSearchMapperInterface


class FilesCompressMapper(FilesCompressMapperInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        files_search_mapper: FilesSearchMapperInterface,
        file_compress_mapper: FileCompressMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.files_search_mapper = files_search_mapper
        self.file_compress_mapper = file_compress_mapper

    def compress(self, file: FileModel, csv_file: FileModel, files: List[FileModel]) -> FileModel:
        filename = Path(csv_file.filename).stem
        extension = Path(file.filename).suffix
        new_filename = f"{filename}{extension}"

        all_files = self.files_search_mapper.search(files=files, search=csv_file.relations)

        self.logger_repository.info(message=f"Compressing {len(all_files)} records in the file {new_filename}.")

        all_files.append(csv_file)

        return self.file_compress_mapper.compress(filename=f"{filename}{extension}", files=all_files)
