import io
from unittest import TestCase
from unittest.mock import MagicMock, patch

from faker import Faker
from pysftp import Connection

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.get_file_gateway import GetFileGateway


class TestGetFileGateway(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.config_mock = MagicMock(SourceConfigRepositoryInterface)
        self.connector_mock = MagicMock(SftpConnectorInterface)
        self.connection_mock = MagicMock(Connection)

        self.gateway = GetFileGateway(
            logger_repository=self.logger_repository_mock,
            config=self.config_mock,
            connector=self.connector_mock,
        )

    def test_should_check_get_full_filename_parameters(self) -> None:
        input_filename = self.faker.word()

        self.gateway.get_file_from_sftp(input_filename)

        self.config_mock.get_source_full_filename.assert_called_once_with(filename=input_filename)

    def test_should_check_get_connection_parameters(self) -> None:
        input_filename = self.faker.word()

        self.gateway.get_file_from_sftp(input_filename)

        self.connector_mock.get_connection.assert_called_once_with(config=self.config_mock)

    def test_should_check_download_parameters(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()
        buffer = MagicMock(io.BytesIO)

        self.config_mock.get_source_full_filename.return_value = full_filename
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock

        with patch("io.BytesIO") as mock_buffer:
            mock_buffer.return_value.__enter__.return_value = buffer
            self.gateway.get_file_from_sftp(input_filename)

        self.connection_mock.getfo.assert_called_once_with(full_filename, buffer)

    def test_should_check_response(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()
        content = self.faker.binary(length=64)

        buffer = MagicMock(io.BytesIO)

        buffer.getvalue.return_value = content
        self.config_mock.get_source_full_filename.return_value = full_filename
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock

        with patch("io.BytesIO") as mock_buffer:
            mock_buffer.return_value.__enter__.return_value = buffer
            response = self.gateway.get_file_from_sftp(input_filename)

            self.assertIsInstance(response, FileModel)
            self.assertEqual(response.filename, input_filename)
            self.assertEqual(response.content, content)

    def test_should_check_logger_info_parameters(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()

        self.config_mock.get_source_full_filename.return_value = full_filename

        with patch("io.BytesIO"):
            self.gateway.get_file_from_sftp(input_filename)

        self.logger_repository_mock.info.assert_called_once_with(message=f"Getting content file from {full_filename}.")

    def test_should_check_throws_exception_when_connection(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()
        exception = Exception("error")

        self.config_mock.get_source_full_filename.return_value = full_filename
        self.connector_mock.get_connection.side_effect = exception

        with patch("io.BytesIO"):
            with self.assertRaises(Exception) as context:
                self.gateway.get_file_from_sftp(input_filename)

            self.assertIsInstance(context.exception, GatewayException)
            self.logger_repository_mock.error.assert_called_once_with(message=f"Error to get file {full_filename} from sftp.", cause=exception)
            self.assertEqual(context.exception.args[0], f"Error to get file {full_filename} from sftp.")
            self.assertEqual(context.exception.args[1], exception)
