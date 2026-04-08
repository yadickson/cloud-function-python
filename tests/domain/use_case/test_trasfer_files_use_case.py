from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.del_files_repository_interface import DelFilesRepositoryInterface
from app.domain.repository.get_files_repository_interface import GetFilesRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.repository.send_files_repository_interface import SendFilesRepositoryInterface
from app.domain.use_case.transfer_files_use_case import TransferFilesUseCase


class TestTransferFilesUseCase(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.get_files_repository_mock = MagicMock(GetFilesRepositoryInterface)
        self.send_files_repository_mock = MagicMock(SendFilesRepositoryInterface)
        self.del_files_repository_mock = MagicMock(DelFilesRepositoryInterface)

        self.use_case = TransferFilesUseCase(
            logger_repository=self.logger_repository_mock,
            get_files_repository=self.get_files_repository_mock,
            send_files_repository=self.send_files_repository_mock,
            del_files_repository=self.del_files_repository_mock,
        )

    def test_should_check_order(self) -> None:
        call_order: List[int] = []

        self.logger_repository_mock.running.side_effect = lambda *a, **kw: call_order.append(1)
        self.get_files_repository_mock.execute.side_effect = lambda *a, **kw: call_order.append(2)
        self.send_files_repository_mock.execute.side_effect = lambda *a, **kw: call_order.append(3)
        self.del_files_repository_mock.execute.side_effect = lambda *a, **kw: call_order.append(4)
        self.logger_repository_mock.success.side_effect = lambda *a, **kw: call_order.append(5)

        self.use_case.execute()

        self.assertSequenceEqual(call_order, [1, 2, 3, 4, 5])

    def test_should_check_running_logger_parameters(self) -> None:
        self.use_case.execute()

        self.logger_repository_mock.running.assert_called_once_with(message="Starting files transfer.")

    def test_should_check_get_file_parameters(self) -> None:
        self.use_case.execute()

        self.get_files_repository_mock.execute.assert_called_once_with()

    def test_should_check_send_file_parameters(self) -> None:
        files = Autodata.create_many(FileModel, 10)

        self.get_files_repository_mock.execute.return_value = files

        self.use_case.execute()

        self.send_files_repository_mock.execute.assert_called_once_with(files=files)

    def test_should_check_success_logger_parameters(self) -> None:
        count = self.faker.random_int(min=5, max=20)
        files = Autodata.create_many(FileModel, count)

        self.get_files_repository_mock.execute.return_value = files

        self.use_case.execute()

        self.logger_repository_mock.success.assert_called_once_with(message=f"Files transferred [{count}].")

    def test_should_check_success_logger_parameters_when_there_are_not_files(self) -> None:
        self.get_files_repository_mock.execute.return_value = []

        self.use_case.execute()

        self.logger_repository_mock.success.assert_called_once_with(message="There are no files to transmit.")
