import zlib

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.mapper_exception import MapperException
from app.infrastructure.mapper.file_decompress_full_mapper_interface import FileDecompressFullMapperInterface
from app.infrastructure.mapper.file_zip_info_mapper_interface import FileZipInfoMapperInterface


class FileDecompressFullMapper(FileDecompressFullMapperInterface):
    @inject
    def __init__(self, logger_repository: LoggerRepositoryInterface, zip_file_info_mapper: FileZipInfoMapperInterface) -> None:
        self.logger_repository = logger_repository
        self.zip_file_info_mapper = zip_file_info_mapper

    def decompress_full(self, content: bytes) -> FileModel:
        try:
            self.logger_repository.info(message=f"Try to decompress full [{len(content)}] bytes.")
            filename = self.zip_file_info_mapper.get_filename(content=content)
            self.logger_repository.info(message=f"Decompress full filename [{filename}].")
            body = self.zip_file_info_mapper.get_body(content=content)
            return FileModel(filename=filename, content=zlib.decompress(body, wbits=-zlib.MAX_WBITS))
        except Exception as exception:
            self.logger_repository.error(message="Error to decompress full content.", cause=exception)
            raise MapperException("Error to decompress full content.", exception)
