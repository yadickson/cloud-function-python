import io
from unittest import TestCase
from unittest.mock import MagicMock, patch

from faker import Faker
from pysftp import Connection

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.destination_config_repository_interface import DestinationConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.send_file_gateway import SendFileGateway


class TestSendFileGateway(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.config_mock = MagicMock(DestinationConfigRepositoryInterface)
        self.connector_mock = MagicMock(SftpConnectorInterface)
        self.connection_mock = MagicMock(Connection)

        self.gateway = SendFileGateway(
            logger_repository=self.logger_repository_mock,
            config=self.config_mock,
            connector=self.connector_mock,
        )

    def test_should_check_get_full_filename_parameters(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        self.gateway.send_file_to_sftp(file)

        self.config_mock.get_destination_full_filename.assert_called_once_with(filename=filename)

    def test_should_check_get_connection_parameters(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        self.gateway.send_file_to_sftp(file)

        self.connector_mock.get_connection.assert_called_once_with(config=self.config_mock)

    def test_should_check_buffer_parameters(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        buffer = MagicMock(io.BytesIO)

        with patch("io.BytesIO") as mock_buffer:
            mock_buffer.return_value.__enter__.return_value = buffer

            self.gateway.send_file_to_sftp(file)

        mock_buffer.assert_called_once_with(content)

    def test_should_check_send_parameters(self) -> None:
        full_filename = self.faker.word()
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        buffer = MagicMock(io.BytesIO)

        self.config_mock.get_destination_full_filename.return_value = full_filename
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock

        with patch("io.BytesIO") as mock_buffer:
            mock_buffer.return_value.__enter__.return_value = buffer

            self.gateway.send_file_to_sftp(file)

        self.connection_mock.putfo.assert_called_once_with(remotepath=full_filename, flo=buffer)

    def test_should_check_logger_info_parameters(self) -> None:
        full_filename = self.faker.word()
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        self.config_mock.get_destination_full_filename.return_value = full_filename

        self.gateway.send_file_to_sftp(file)

        call_count = self.logger_repository_mock.info.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.logger_repository_mock.info.call_args_list

        self.assertEqual(call_args_list[0][1], {"message": f"Uploading {full_filename} file to sftp server."})
        self.assertEqual(call_args_list[1][1], {"message": f"Uploaded {full_filename} to sftp server."})

    def test_should_check_throws_exception_when_connection_fail(self) -> None:
        directory = self.faker.word()
        exception = Exception("error")
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        self.config_mock.get_destination_full_filename.return_value = directory
        self.connector_mock.get_connection.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.gateway.send_file_to_sftp(file)

        self.assertIsInstance(context.exception, GatewayException)
        self.logger_repository_mock.error.assert_called_once_with(message=f"Error to send file {filename} to sftp server.", cause=exception)
        self.assertEqual(context.exception.args[0], f"Error to send file {filename} to sftp server.")
        self.assertEqual(context.exception.args[1], exception)
