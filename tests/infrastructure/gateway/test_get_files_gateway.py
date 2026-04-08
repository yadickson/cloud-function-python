from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker
from pysftp import Connection

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.exception.gateway_exception import GatewayException
from app.infrastructure.gateway.get_files_gateway import GetFilesGateway
from app.infrastructure.mapper.files_filtered_mapper_interface import FilesFilteredMapperInterface


class TestGetFilesGateway(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.config_mock = MagicMock(SourceConfigRepositoryInterface)
        self.connector_mock = MagicMock(SftpConnectorInterface)
        self.connection_mock = MagicMock(Connection)
        self.files_filtered_mapper = MagicMock(FilesFilteredMapperInterface)

        self.gateway = GetFilesGateway(
            logger_repository=self.logger_repository_mock,
            config=self.config_mock,
            connector=self.connector_mock,
            files_filtered_mapper=self.files_filtered_mapper,
        )

    def test_should_check_get_connection_parameters(self) -> None:
        self.gateway.get_files_from_sftp()
        self.connector_mock.get_connection.assert_called_once_with(config=self.config_mock)

    def test_should_check_listdir_parameters(self) -> None:
        directory = self.faker.word()

        self.config_mock.get_source_directory.return_value = directory
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock

        self.gateway.get_files_from_sftp()

        self.connection_mock.listdir.assert_called_once_with(directory)

    def test_should_check_empty_response_when_filtered_are_empty(self) -> None:
        directory = self.faker.word()
        remote_file_one = self.faker.word()
        remote_file_two = self.faker.word()

        self.config_mock.get_source_directory.return_value = directory
        self.connection_mock.listdir.return_value = [remote_file_one, remote_file_two]
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock
        self.files_filtered_mapper.filter.return_value = []

        response = self.gateway.get_files_from_sftp()

        self.assertListEqual(response, [])
        self.files_filtered_mapper.filter.assert_called_once_with([remote_file_one, remote_file_two])

    def test_should_check_response(self) -> None:
        directory = self.faker.word()
        remote_file_one = self.faker.word()
        remote_file_two = self.faker.word()
        filtered_one = self.faker.word()
        filtered_two = self.faker.word()

        self.config_mock.get_source_directory.return_value = directory
        self.connection_mock.listdir.return_value = [remote_file_one, remote_file_two]
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock
        self.files_filtered_mapper.filter.return_value = [filtered_one, filtered_two]

        response = self.gateway.get_files_from_sftp()

        self.assertListEqual(response, [filtered_one, filtered_two])
        self.files_filtered_mapper.filter.assert_called_once_with([remote_file_one, remote_file_two])

    def test_should_check_logger_info_parameters(self) -> None:
        directory = self.faker.word()
        files = self.faker.get_words_list()

        self.config_mock.get_source_directory.return_value = directory
        self.connection_mock.listdir.return_value = files
        self.connector_mock.get_connection.return_value.__enter__.return_value = self.connection_mock

        self.gateway.get_files_from_sftp()

        call_count = self.logger_repository_mock.info.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.logger_repository_mock.info.call_args_list

        self.assertEqual(call_args_list[0][1], {"message": f"Searching files from {directory}."})
        self.assertEqual(call_args_list[1][1], {"message": f"Files found: {files}."})

    def test_should_check_throws_exception_when_connection(self) -> None:
        directory = self.faker.word()
        exception = Exception("error")

        self.config_mock.get_source_directory.return_value = directory
        self.connector_mock.get_connection.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.gateway.get_files_from_sftp()

        self.assertIsInstance(context.exception, GatewayException)
        self.logger_repository_mock.error.assert_called_once_with(message=f"Error to get files from {directory}.", cause=exception)
        self.assertEqual(context.exception.args[0], f"Error to get files from {directory}.")
        self.assertEqual(context.exception.args[1], exception)
