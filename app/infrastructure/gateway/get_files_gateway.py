from typing import List

from injector import inject

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.get_files_gateway_interface import GetFilesGatewayInterface
from app.infrastructure.mapper.files_filtered_mapper_interface import FilesFilteredMapperInterface


class GetFilesGateway(GetFilesGatewayInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        config: SourceConfigRepositoryInterface,
        connector: SftpConnectorInterface,
        files_filtered_mapper: FilesFilteredMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.config = config
        self.connector = connector
        self.files_filtered_mapper = files_filtered_mapper

    def get_files_from_sftp(self) -> List[str]:
        source_directory = self.config.get_source_directory()

        try:
            with self.connector.get_connection(config=self.config) as connection:
                self.logger_repository.info(message=f"Searching files from {source_directory}.")

                files = connection.listdir(source_directory)

                self.logger_repository.info(message=f"Files found: {files}.")

                return self.files_filtered_mapper.filter([file for file in files])

        except Exception as exception:
            self.logger_repository.error(message=f"Error to get files from {source_directory}.", cause=exception)
            raise GatewayException(f"Error to get files from {source_directory}.", exception)
