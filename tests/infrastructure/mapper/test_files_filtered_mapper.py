from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.infrastructure.mapper.files_filtered_mapper import FilesFilteredMapper
from app.infrastructure.mapper.files_filters_mapper_interface import FilesFiltersMapperInterface


class TestFilesFilteredMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.files_filters_mapper_mock = MagicMock(FilesFiltersMapperInterface)

        self.mapper = FilesFilteredMapper(
            files_filters_mapper=self.files_filters_mapper_mock,
        )

    def test_should_check_get_files_parameters(self) -> None:
        files = self.faker.words(10)

        self.mapper.filter(files)

        self.files_filters_mapper_mock.get_files.assert_called_once_with()

    def test_should_check_response_with_all_files(self) -> None:
        file_one = "fIle_One_1234.Zip"
        file_two = "file_two_1234.zip"

        file_filter = "file_.*.zip"

        self.files_filters_mapper_mock.get_files.return_value = [file_filter]

        response = self.mapper.filter([file_one, file_two])

        self.assertListEqual(response, [file_one, file_two])
