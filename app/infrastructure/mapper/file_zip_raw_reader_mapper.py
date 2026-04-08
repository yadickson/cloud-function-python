from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_decompress_mapper_interface import FileDecompressMapperInterface
from app.infrastructure.mapper.file_zip_raw_reader_mapper_interface import FileZipRawReaderMapperInterface
from app.infrastructure.mapper.file_zip_raw_split_mapper_interface import FileZipRawSplitMapperInterface


class FileZipRawReaderMapper(FileZipRawReaderMapperInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        file_zip_raw_split_mapper: FileZipRawSplitMapperInterface,
        decompress_mapper: FileDecompressMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.file_zip_raw_split_mapper = file_zip_raw_split_mapper
        self.decompress_mapper = decompress_mapper

    def read(self, file: FileModel) -> List[FileModel]:
        self.logger_repository.info(message=f"Reading raw {file.filename} file.")
        contents = self.file_zip_raw_split_mapper.get_parts(content=file.content)
        self.logger_repository.info(message=f"Found {len(contents)} files.")
        return [self.decompress_mapper.decompress(content=content) for content in contents]
