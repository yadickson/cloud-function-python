from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_decompress_full_mapper_interface import FileDecompressFullMapperInterface
from app.infrastructure.mapper.file_decompress_mapper_interface import FileDecompressMapperInterface
from app.infrastructure.mapper.file_decompress_raw_mapper_interface import FileDecompressRawMapperInterface


class FileDecompressMapper(FileDecompressMapperInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        decompress_full_mapper: FileDecompressFullMapperInterface,
        decompress_raw_mapper: FileDecompressRawMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.decompress_full_mapper = decompress_full_mapper
        self.decompress_raw_mapper = decompress_raw_mapper

    def decompress(self, content: bytes) -> FileModel:
        try:
            return self.decompress_full_mapper.decompress_full(content=content)
        except Exception as exception:
            self.logger_repository.error(message="Error to decompress content.", cause=exception)
            return self.decompress_raw_mapper.decompress_raw(content=content)
