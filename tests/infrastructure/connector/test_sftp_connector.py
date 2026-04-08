from unittest import TestCase
from unittest.mock import MagicMock, patch

import pysftp
from faker import Faker

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.connector_config_repository_interface import ConnectorConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector import SftpConnector
from app.infrastructure.connector.sftp_connector_options_interface import SftpConnectorOptionsInterface
from app.infrastructure.exception.connector_exception import ConnectorException


class TestSftpConnector(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.config_mock = MagicMock(ConnectorConfigRepositoryInterface)
        self.options_mock = MagicMock(SftpConnectorOptionsInterface)

        self.connector = SftpConnector(
            logger_repository=self.logger_repository_mock,
            options=self.options_mock,
        )

    def test_should_check_sftp_parameters(self) -> None:
        host = self.faker.word()
        port = self.faker.random_int()
        username = self.faker.word()
        password = self.faker.word()
        options = MagicMock(pysftp.CnOpts)

        self.config_mock.get_host.return_value = host
        self.config_mock.get_port.return_value = port
        self.config_mock.get_username.return_value = username
        self.config_mock.get_password.return_value = password
        self.options_mock.get_options.return_value = options

        with patch("pysftp.Connection") as mock_instance:
            self.connector.get_connection(self.config_mock)

        mock_instance.assert_called_once_with(host=host, port=port, username=username, password=password, cnopts=options)

    def test_should_check_logger_info_parameters(self) -> None:
        host = self.faker.word()
        port = self.faker.random_int()

        self.config_mock.get_host.return_value = host
        self.config_mock.get_port.return_value = port

        with patch("pysftp.Connection"):
            self.connector.get_connection(self.config_mock)

        self.logger_repository_mock.info.assert_called_once_with(message=f"Connecting to sftp://{host}:{port} server.")

    def test_should_check_throws_exception_when_ftp_fail(self) -> None:
        host = self.faker.word()
        port = self.faker.random_int()
        exception = Exception("error")

        self.config_mock.get_host.return_value = host
        self.config_mock.get_port.return_value = port

        with patch("pysftp.Connection") as mock_instance:
            mock_instance.side_effect = exception

            with self.assertRaises(Exception) as context:
                self.connector.get_connection(self.config_mock)

        self.assertIsInstance(context.exception, ConnectorException)
        self.logger_repository_mock.error.assert_called_once_with(message=f"Error to connected to sftp://{host}:{port} server.", cause=exception)
        self.assertEqual(context.exception.args[0], "Error to connected to sftp server.")
        self.assertEqual(context.exception.args[1], exception)
