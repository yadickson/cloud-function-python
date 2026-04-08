import io

from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.get_file_gateway_interface import GetFileGatewayInterface


class GetFileGateway(GetFileGatewayInterface):
    @inject
    def __init__(
        self, logger_repository: LoggerRepositoryInterface, config: SourceConfigRepositoryInterface, connector: SftpConnectorInterface
    ) -> None:
        self.logger_repository = logger_repository
        self.config = config
        self.connector = connector

    def get_file_from_sftp(self, filename: str) -> FileModel:
        full_filename = self.config.get_source_full_filename(filename=filename)

        try:
            with self.connector.get_connection(config=self.config) as connection:
                with io.BytesIO() as buffer_file:
                    self.logger_repository.info(message=f"Getting content file from {full_filename}.")
                    connection.getfo(full_filename, buffer_file)
                    return FileModel(filename=filename, content=buffer_file.getvalue())

        except Exception as exception:
            self.logger_repository.error(message=f"Error to get file {full_filename} from sftp.", cause=exception)
            raise GatewayException(f"Error to get file {full_filename} from sftp.", exception)
