from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_mapper_interface import FileMapperInterface
from app.infrastructure.mapper.files_mapper import FilesMapper


class TestFilesMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.file_mapper_mock = MagicMock(FileMapperInterface)
        self.mapper = FilesMapper(file_mapper=self.file_mapper_mock)

    def test_should_check_empty_response_when_response_empty(self) -> None:
        files = Autodata.create_many(FileModel, 10)

        self.file_mapper_mock.get_files.return_value = []

        response = self.mapper.get_files(files=files)
        self.assertListEqual(response, [])

    def test_should_check_response_from_multiple_files(self) -> None:
        files = Autodata.create_many(FileModel, 2)
        files_one = Autodata.create_many(FileModel, 10)
        files_two = Autodata.create_many(FileModel, 15)

        self.file_mapper_mock.get_files.side_effect = [files_one, files_two]

        response = self.mapper.get_files(files=files)

        self.assertEqual(len(response), len(files_one) + len(files_two))

    def test_should_get_files_parameters(self) -> None:
        files = Autodata.create_many(FileModel, 2)
        files_one = Autodata.create_many(FileModel, 10)
        files_two = Autodata.create_many(FileModel, 15)

        self.file_mapper_mock.get_files.side_effect = [files_one, files_two]

        self.mapper.get_files(files=files)

        call_count = self.file_mapper_mock.get_files.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.file_mapper_mock.get_files.call_args_list

        self.assertEqual(call_args_list[0][1], {"file": files[0]})
        self.assertEqual(call_args_list[1][1], {"file": files[1]})
