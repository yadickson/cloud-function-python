import io

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.destination_config_repository_interface import DestinationConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.send_file_gateway_interface import SendFileGatewayInterface


class SendFileGateway(SendFileGatewayInterface):
    @inject
    def __init__(
        self, logger_repository: LoggerRepositoryInterface, config: DestinationConfigRepositoryInterface, connector: SftpConnectorInterface
    ) -> None:
        self.logger_repository = logger_repository
        self.config = config
        self.connector = connector

    def send_file_to_sftp(self, file: FileModel) -> None:
        filename = file.filename
        dest_full_filename = self.config.get_destination_full_filename(filename=filename)

        try:
            with self.connector.get_connection(config=self.config) as connection:
                self.logger_repository.info(message=f"Uploading {dest_full_filename} file to sftp server.")

                with io.BytesIO(file.content) as buffer_file:
                    connection.putfo(remotepath=dest_full_filename, flo=buffer_file)

                self.logger_repository.info(message=f"Uploaded {dest_full_filename} to sftp server.")

        except Exception as exception:
            self.logger_repository.error(message=f"Error to send file {filename} to sftp server.", cause=exception)
            raise GatewayException(f"Error to send file {filename} to sftp server.", exception)
