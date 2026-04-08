import pysftp
from injector import inject

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.connector_config_repository_interface import ConnectorConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.connector.sftp_connector_options_interface import SftpConnectorOptionsInterface
from app.infrastructure.exception.connector_exception import ConnectorException


class SftpConnector(SftpConnectorInterface):
    @inject
    def __init__(self, logger_repository: LoggerRepositoryInterface, options: SftpConnectorOptionsInterface) -> None:
        self.logger_repository = logger_repository
        self.options = options

    def get_connection(self, config: ConnectorConfigRepositoryInterface) -> pysftp.Connection:
        source_host = config.get_host()
        source_port = config.get_port()
        source_username = config.get_username()
        source_password = config.get_password()
        options = self.options.get_options()

        try:
            self.logger_repository.info(message=f"Connecting to sftp://{source_host}:{source_port} server.")
            return pysftp.Connection(host=source_host, port=source_port, username=source_username, password=source_password, cnopts=options)

        except Exception as exception:
            self.logger_repository.error(message=f"Error to connected to sftp://{source_host}:{source_port} server.", cause=exception)
            raise ConnectorException("Error to connected to sftp server.", exception)
