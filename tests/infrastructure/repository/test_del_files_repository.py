from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.repository_exception import RepositoryException
from app.infrastructure.gateway.del_file_gateway_interface import DelFileGatewayInterface
from app.infrastructure.gateway.get_files_gateway_interface import GetFilesGatewayInterface
from app.infrastructure.repository.del_files_repository import DelFilesRepository


class TestDelFilesRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.get_files_gateway_mock = MagicMock(GetFilesGatewayInterface)
        self.del_file_gateway_mock = MagicMock(DelFileGatewayInterface)

        self.repository = DelFilesRepository(
            logger_repository=self.logger_repository_mock,
            get_files_gateway=self.get_files_gateway_mock,
            del_file_gateway=self.del_file_gateway_mock,
        )

    def test_should_check_logger_parameters(self) -> None:
        files = self.faker.get_words_list()

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files

        self.repository.execute()

        self.logger_repository_mock.info.assert_called_once_with(message="Remove files from gateway.")

    def test_should_check_get_files_gateway_parameters(self) -> None:
        files = self.faker.get_words_list()

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files

        self.repository.execute()

        self.get_files_gateway_mock.get_files_from_sftp.assert_called_once_with()

    def test_should_check_del_file_gateway_parameters(self) -> None:
        filename = self.faker.word()
        files = [filename]

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files

        self.repository.execute()

        self.del_file_gateway_mock.del_file_from_sftp.assert_called_once_with(filename=filename)

    def test_should_check_throws_exception_when_gateway_fail(self) -> None:
        exception = Exception("error")

        self.get_files_gateway_mock.get_files_from_sftp.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.repository.execute()

        self.assertIsInstance(context.exception, RepositoryException)
        self.logger_repository_mock.error.assert_called_once_with(message="Error to remove files from gateway.", cause=exception)
        self.assertEqual(context.exception.args[0], "Error to remove files from gateway.")
        self.assertEqual(context.exception.args[1], exception)
