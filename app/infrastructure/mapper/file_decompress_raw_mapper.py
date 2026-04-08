import zlib

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.mapper_exception import MapperException
from app.infrastructure.mapper.file_decompress_raw_mapper_interface import FileDecompressRawMapperInterface
from app.infrastructure.mapper.file_zip_info_mapper_interface import FileZipInfoMapperInterface


class FileDecompressRawMapper(FileDecompressRawMapperInterface):
    @inject
    def __init__(self, logger_repository: LoggerRepositoryInterface, zip_file_info_mapper: FileZipInfoMapperInterface) -> None:
        self.logger_repository = logger_repository
        self.zip_file_info_mapper = zip_file_info_mapper

    def decompress_raw(self, content: bytes) -> FileModel:
        try:
            self.logger_repository.info(message=f"Try to decompress raw [{len(content)}] bytes.")
            filename = self.zip_file_info_mapper.get_filename(content=content)
            self.logger_repository.info(message=f"Decompress raw filename [{filename}].")
            body = self.zip_file_info_mapper.get_body(content=content)

            chunk = 10  # pragma: no mutate
            decompressor = zlib.decompressobj(wbits=-zlib.MAX_WBITS)

            chunks = [decompressor.decompress(body[i : i + chunk]) for i in range(0, len(body), chunk)]  # pragma: no mutate
            chunks.append(decompressor.flush())

            return FileModel(filename=filename, content=b"".join(chunks))  # pragma: no mutate
        except Exception as exception:
            self.logger_repository.error(message="Error to decompress raw content.", cause=exception)
            raise MapperException("Error to decompress raw content.", exception)
