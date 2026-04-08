from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.domain.model.file_model import FileModel
from app.infrastructure.configuration.destination_config_repository_interface import DestinationConfigRepositoryInterface
from app.infrastructure.mapper.file_csv_group_mapper import FileCsvGroupMapper


class TestFileCsvGroupMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.config_mock = MagicMock(DestinationConfigRepositoryInterface)

        self.mapper = FileCsvGroupMapper(config=self.config_mock)

    def test_should_check_empty_response_when_content_is_empty(self) -> None:
        filename = self.faker.word()
        content = b""

        file = FileModel(filename=filename, content=content)

        response = self.mapper.group(file=file)

        self.assertListEqual(response, [])

    def test_should_check_one_line_response_when_content_only_has_two_lines_and_max_is_ten(self) -> None:
        filename = self.faker.word()
        content = "Hello\nWorld".encode("utf-8")

        self.config_mock.get_destination_file_max_registers.return_value = 10

        file = FileModel(filename=filename, content=content)

        response = self.mapper.group(file=file)

        self.assertListEqual(response, [[b"Hello", b"World"]])

    def test_should_check_one_line_response_when_content_only_has_two_lines_and_mas_is_one(self) -> None:
        filename = self.faker.word()
        content = "Hello\nWorld".encode("utf-8")

        self.config_mock.get_destination_file_max_registers.return_value = 1

        file = FileModel(filename=filename, content=content)

        response = self.mapper.group(file=file)

        self.assertListEqual(response, [[b"Hello"], [b"World"]])
