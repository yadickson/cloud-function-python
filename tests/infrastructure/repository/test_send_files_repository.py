from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.repository_exception import RepositoryException
from app.infrastructure.gateway.send_file_gateway_interface import SendFileGatewayInterface
from app.infrastructure.repository.send_files_repository import SendFilesRepository


class TestSendFilesRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.gateway_mock = MagicMock(SendFileGatewayInterface)

        self.repository = SendFilesRepository(
            logger_repository=self.logger_repository_mock,
            gateway=self.gateway_mock,
        )

    def test_should_check_order_when_send_only_one_file(self) -> None:
        call_order: List[int] = []
        files = Autodata.create_many(FileModel, 1)

        self.logger_repository_mock.info.side_effect = lambda *a, **kw: call_order.append(1)
        self.gateway_mock.send_file_to_sftp.side_effect = lambda *a, **kw: call_order.append(2)

        self.repository.execute(files=files)

        self.assertSequenceEqual(call_order, [1, 2])

    def test_should_check_logger_parameters(self) -> None:
        files = Autodata.create_many(FileModel, 10)

        self.repository.execute(files=files)

        self.logger_repository_mock.info.assert_called_once_with(message="Sending files to gateway.")

    def test_should_check_gateway_parameters_when_send_one_file(self) -> None:
        file_mock = Autodata.create(FileModel)
        files = [file_mock]

        self.repository.execute(files=files)

        self.gateway_mock.send_file_to_sftp.assert_called_once_with(file=file_mock)

    def test_should_check_gateway_parameters_when_send_two_files(self) -> None:
        file_one_mock = Autodata.create(FileModel)
        file_two_mock = Autodata.create(FileModel)

        files = [file_one_mock, file_two_mock]

        self.repository.execute(files=files)

        call_count = self.gateway_mock.send_file_to_sftp.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.gateway_mock.send_file_to_sftp.call_args_list

        self.assertEqual(call_args_list[0][1], {"file": file_one_mock})
        self.assertEqual(call_args_list[1][1], {"file": file_two_mock})

    def test_should_check_throws_exception_when_gateway_fail(self) -> None:
        files = Autodata.create_many(FileModel, 10)

        exception = Exception("error")

        self.gateway_mock.send_file_to_sftp.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.repository.execute(files=files)

        self.assertIsInstance(context.exception, RepositoryException)
        self.logger_repository_mock.error.assert_called_once_with(message="Error to send files to gateway.", cause=exception)
        self.assertEqual(context.exception.args[0], "Error to send files to gateway.")
        self.assertEqual(context.exception.args[1], exception)
