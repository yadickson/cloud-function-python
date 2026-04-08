from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.repository_exception import RepositoryException
from app.infrastructure.gateway.get_file_gateway_interface import GetFileGatewayInterface
from app.infrastructure.gateway.get_files_gateway_interface import GetFilesGatewayInterface
from app.infrastructure.mapper.file_crypto_mapper_interface import FileCryptoMapperInterface
from app.infrastructure.mapper.files_mapper_interface import FilesMapperInterface
from app.infrastructure.repository.get_files_repository import GetFilesRepository


class TestGetFilesRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.get_files_gateway_mock = MagicMock(GetFilesGatewayInterface)
        self.get_file_gateway_mock = MagicMock(GetFileGatewayInterface)
        self.files_mapper_mock = MagicMock(FilesMapperInterface)
        self.file_crypto_mapper_mock = MagicMock(FileCryptoMapperInterface)

        self.repository = GetFilesRepository(
            logger_repository=self.logger_repository_mock,
            get_files_gateway=self.get_files_gateway_mock,
            get_file_gateway=self.get_file_gateway_mock,
            files_mapper=self.files_mapper_mock,
            file_crypto_mapper=self.file_crypto_mapper_mock,
        )

    def test_should_check_logger_parameters(self) -> None:
        files = self.faker.get_words_list()

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files

        self.repository.execute()

        self.logger_repository_mock.info.assert_called_once_with(message="Getting files from gateway.")

    def test_should_check_get_files_gateway_parameters(self) -> None:
        files = self.faker.get_words_list()

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files

        self.repository.execute()

        self.get_files_gateway_mock.get_files_from_sftp.assert_called_once_with()

    def test_should_check_get_file_gateway_parameters(self) -> None:
        filename = self.faker.word()
        files = [filename]
        file = Autodata.create_many(FileModel)

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files
        self.get_file_gateway_mock.get_file_from_sftp.return_value = file

        self.repository.execute()

        self.get_file_gateway_mock.get_file_from_sftp.assert_called_once_with(filename=filename)

    def test_should_check_mapper_parameters(self) -> None:
        filename = self.faker.word()
        files = [filename]
        file = Autodata.create_many(FileModel)

        self.get_files_gateway_mock.get_files_from_sftp.return_value = files
        self.get_file_gateway_mock.get_file_from_sftp.return_value = file

        self.repository.execute()

        self.files_mapper_mock.get_files.assert_called_once_with(files=[file])

    def test_should_check_response(self) -> None:
        files = Autodata.create_many(FileModel, 10)
        encode = Autodata.create(FileModel)

        self.files_mapper_mock.get_files.return_value = files
        self.file_crypto_mapper_mock.encode.return_value = encode

        response = self.repository.execute()

        self.assertEqual(len(response), 10)

    def test_should_crypto_parameters(self) -> None:
        files = Autodata.create_many(FileModel, 2)
        encode = Autodata.create(FileModel)

        self.files_mapper_mock.get_files.return_value = files
        self.file_crypto_mapper_mock.encode.return_value = encode

        self.repository.execute()

        call_count = self.file_crypto_mapper_mock.encode.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.file_crypto_mapper_mock.encode.call_args_list

        self.assertEqual(call_args_list[0][1], {"file": files[0]})
        self.assertEqual(call_args_list[1][1], {"file": files[1]})

    def test_should_check_throws_exception_when_gateway_fail(self) -> None:
        exception = Exception("error")

        self.get_files_gateway_mock.get_files_from_sftp.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.repository.execute()

        self.assertIsInstance(context.exception, RepositoryException)
        self.logger_repository_mock.error.assert_called_once_with(message="Error to get files from gateway.", cause=exception)
        self.assertEqual(context.exception.args[0], "Error to get files from gateway.")
        self.assertEqual(context.exception.args[1], exception)
