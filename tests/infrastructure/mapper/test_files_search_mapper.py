from unittest import TestCase

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.files_search_mapper import FilesSearchMapper


class TestFilesSearchMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.mapper = FilesSearchMapper()

    def test_should_check_all_response(self) -> None:
        files = Autodata.create_many(FileModel, 10)
        file_list = [file.filename for file in files]
        response = self.mapper.search(files=files, search=file_list)
        self.assertListEqual(response, files)

    def test_should_check_filter_response(self) -> None:
        file_one = FileModel(filename="abcd", content=b"")
        file_two = FileModel(filename="1234", content=b"")

        files = [file_one, file_two]
        file_list = ["1234"]

        response = self.mapper.search(files=files, search=file_list)

        self.assertListEqual(response, [file_two])
