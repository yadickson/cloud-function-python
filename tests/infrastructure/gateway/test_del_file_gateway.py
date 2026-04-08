from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker
from pysftp import Connection

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.del_file_gateway import DelFileGateway


class TestDelFileGateway(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.config_mock = MagicMock(SourceConfigRepositoryInterface)
        self.connector_mock = MagicMock(SftpConnectorInterface)
        self.connection_mock = MagicMock(Connection)

        self.gateway = DelFileGateway(
            logger_repository=self.logger_repository_mock,
            config=self.config_mock,
            connector=self.connector_mock,
        )

    def test_should_check_get_full_filename_parameters(self) -> None:
        input_filename = self.faker.word()

        self.gateway.del_file_from_sftp(input_filename)

        self.config_mock.get_source_full_filename.assert_called_once_with(filename=input_filename)

    def test_should_check_get_connection_parameters(self) -> None:
        input_filename = self.faker.word()

        self.gateway.del_file_from_sftp(input_filename)

        self.connector_mock.get_connection.assert_called_once_with(config=self.config_mock)

    def test_should_check_remove_parameters(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()

        self.config_mock.get_source_full_filename.return_value = full_filename
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock

        self.gateway.del_file_from_sftp(input_filename)

        self.connection_mock.remove.assert_called_once_with(full_filename)

    def test_should_check_logger_info_parameters(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()

        self.config_mock.get_source_full_filename.return_value = full_filename

        self.gateway.del_file_from_sftp(input_filename)

        self.logger_repository_mock.info.assert_called_once_with(message=f"Remove file from {full_filename}.")

    def test_should_check_throws_exception_when_connection(self) -> None:
        input_filename = self.faker.word()
        full_filename = self.faker.word()
        exception = Exception("error")

        self.config_mock.get_source_full_filename.return_value = full_filename
        self.connector_mock.get_connection.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.gateway.del_file_from_sftp(input_filename)

        self.assertIsInstance(context.exception, GatewayException)
        self.logger_repository_mock.error.assert_called_once_with(message=f"Error to remove file {full_filename} from sftp.", cause=exception)
        self.assertEqual(context.exception.args[0], f"Error to remove file {full_filename} from sftp.")
        self.assertEqual(context.exception.args[1], exception)
