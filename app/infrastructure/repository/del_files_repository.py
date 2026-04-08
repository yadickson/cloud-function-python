from injector import inject

from app.domain.repository.del_files_repository_interface import DelFilesRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.repository_exception import RepositoryException
from app.infrastructure.gateway.del_file_gateway_interface import DelFileGatewayInterface
from app.infrastructure.gateway.get_files_gateway_interface import GetFilesGatewayInterface


class DelFilesRepository(DelFilesRepositoryInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        get_files_gateway: GetFilesGatewayInterface,
        del_file_gateway: DelFileGatewayInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.get_files_gateway = get_files_gateway
        self.del_file_gateway = del_file_gateway

    def execute(self) -> None:
        try:
            self.logger_repository.info(message="Remove files from gateway.")

            file_lists = self.get_files_gateway.get_files_from_sftp()

            [self.del_file_gateway.del_file_from_sftp(filename=file) for file in file_lists]

        except Exception as exception:
            self.logger_repository.error(message="Error to remove files from gateway.", cause=exception)
            raise RepositoryException("Error to remove files from gateway.", exception)
