from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.get_files_repository_interface import GetFilesRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.repository_exception import RepositoryException
from app.infrastructure.gateway.get_file_gateway_interface import GetFileGatewayInterface
from app.infrastructure.gateway.get_files_gateway_interface import GetFilesGatewayInterface
from app.infrastructure.mapper.file_crypto_mapper_interface import FileCryptoMapperInterface
from app.infrastructure.mapper.files_mapper_interface import FilesMapperInterface


class GetFilesRepository(GetFilesRepositoryInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        get_files_gateway: GetFilesGatewayInterface,
        get_file_gateway: GetFileGatewayInterface,
        files_mapper: FilesMapperInterface,
        file_crypto_mapper: FileCryptoMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.get_files_gateway = get_files_gateway
        self.get_file_gateway = get_file_gateway
        self.files_mapper = files_mapper
        self.file_crypto_mapper = file_crypto_mapper

    def execute(self) -> List[FileModel]:
        try:
            self.logger_repository.info(message="Getting files from gateway.")

            file_lists = self.get_files_gateway.get_files_from_sftp()

            files = [self.get_file_gateway.get_file_from_sftp(filename=file) for file in file_lists]

            return [self.file_crypto_mapper.encode(file=file) for file in self.files_mapper.get_files(files=files)]

        except Exception as exception:
            self.logger_repository.error(message="Error to get files from gateway.", cause=exception)
            raise RepositoryException("Error to get files from gateway.", exception)
