from injector import inject

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.del_file_gateway_interface import DelFileGatewayInterface


class DelFileGateway(DelFileGatewayInterface):
    @inject
    def __init__(
        self, logger_repository: LoggerRepositoryInterface, config: SourceConfigRepositoryInterface, connector: SftpConnectorInterface
    ) -> None:
        self.logger_repository = logger_repository
        self.config = config
        self.connector = connector

    def del_file_from_sftp(self, filename: str) -> None:
        remove_filename = self.config.get_source_full_filename(filename=filename)

        try:
            with self.connector.get_connection(config=self.config) as connection:
                self.logger_repository.info(message=f"Remove file from {remove_filename}.")
                connection.remove(remove_filename)

        except Exception as exception:
            self.logger_repository.error(message=f"Error to remove file {remove_filename} from sftp.", cause=exception)
            raise GatewayException(f"Error to remove file {remove_filename} from sftp.", exception)
