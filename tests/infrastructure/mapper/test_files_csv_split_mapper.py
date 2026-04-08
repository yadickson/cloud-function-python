from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_csv_split_mapper_interface import FileCsvSplitMapperInterface
from app.infrastructure.mapper.files_csv_split_mapper import FilesCsvSplitMapper


class TestFilesCsvSplitMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.file_csv_split_mapper_mock = MagicMock(FileCsvSplitMapperInterface)
        self.mapper = FilesCsvSplitMapper(file_csv_split_mapper=self.file_csv_split_mapper_mock)

    def test_should_check_empty_response_when_split_response_empty(self) -> None:
        files = Autodata.create_many(FileModel, 10)

        self.file_csv_split_mapper_mock.split.return_value = []

        response = self.mapper.split(files=files)
        self.assertListEqual(response, [])

    def test_should_check_response_from_multiple_files(self) -> None:
        files = Autodata.create_many(FileModel, 2)
        files_one = Autodata.create_many(FileModel, 10)
        files_two = Autodata.create_many(FileModel, 15)

        self.file_csv_split_mapper_mock.split.side_effect = [files_one, files_two]

        response = self.mapper.split(files=files)

        self.assertEqual(len(response), len(files_one) + len(files_two))

    def test_should_split_parameters(self) -> None:
        files = Autodata.create_many(FileModel, 2)
        files_one = Autodata.create_many(FileModel, 10)
        files_two = Autodata.create_many(FileModel, 15)

        self.file_csv_split_mapper_mock.split.side_effect = [files_one, files_two]

        self.mapper.split(files=files)

        call_count = self.file_csv_split_mapper_mock.split.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.file_csv_split_mapper_mock.split.call_args_list

        self.assertEqual(call_args_list[0][1], {"file": files[0]})
        self.assertEqual(call_args_list[1][1], {"file": files[1]})
