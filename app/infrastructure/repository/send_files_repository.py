from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.repository.send_files_repository_interface import SendFilesRepositoryInterface
from app.infrastructure.exception.repository_exception import RepositoryException
from app.infrastructure.gateway.send_file_gateway_interface import SendFileGatewayInterface


class SendFilesRepository(SendFilesRepositoryInterface):
    @inject
    def __init__(self, logger_repository: LoggerRepositoryInterface, gateway: SendFileGatewayInterface) -> None:
        self.logger_repository = logger_repository
        self.gateway = gateway

    def execute(self, files: List[FileModel]) -> None:
        try:
            self.logger_repository.info(message="Sending files to gateway.")
            [self.gateway.send_file_to_sftp(file=file) for file in files]

        except Exception as exception:
            self.logger_repository.error(message="Error to send files to gateway.", cause=exception)
            raise RepositoryException("Error to send files to gateway.", exception)
