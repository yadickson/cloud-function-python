from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_compress_mapper_interface import FileCompressMapperInterface
from app.infrastructure.mapper.files_compress_mapper import FilesCompressMapper
from app.infrastructure.mapper.files_search_mapper_interface import FilesSearchMapperInterface


class TestFilesCompressMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.files_search_mapper_mock = MagicMock(FilesSearchMapperInterface)
        self.file_compress_mapper_mock = MagicMock(FileCompressMapperInterface)
        self.mapper = FilesCompressMapper(
            logger_repository=self.logger_repository_mock,
            files_search_mapper=self.files_search_mapper_mock,
            file_compress_mapper=self.file_compress_mapper_mock,
        )

    def test_should_check_files_search_mapper_parameters(self) -> None:
        file = Autodata.create(FileModel)
        csv_file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 10)
        files_filtered = Autodata.create_many(FileModel, 5)

        self.files_search_mapper_mock.search.return_value = files_filtered

        self.mapper.compress(file=file, csv_file=csv_file, files=files)

        self.files_search_mapper_mock.search.assert_called_once_with(files=files, search=csv_file.relations)

    def test_should_check_file_compress_mapper_parameters(self) -> None:
        zip_filename = self.faker.word()
        zip_extension = self.faker.word()
        csv_filename = self.faker.word()
        csv_extension = self.faker.word()

        file = FileModel(filename=f"{zip_filename}.{zip_extension}", content=b"")
        csv_file = FileModel(filename=f"{csv_filename}.{csv_extension}", content=b"")

        files = Autodata.create_many(FileModel, 10)
        files_filtered = Autodata.create_many(FileModel, 5)

        self.files_search_mapper_mock.search.return_value = files_filtered

        self.mapper.compress(file=file, csv_file=csv_file, files=files)

        self.assertEqual(len(files_filtered), 6)
        self.assertTrue(csv_file in files_filtered)
        self.logger_repository_mock.info.assert_called_once_with(message=f"Compressing 5 records in the file {csv_filename}.{zip_extension}.")
        self.file_compress_mapper_mock.compress.assert_called_once_with(filename=f"{csv_filename}.{zip_extension}", files=files_filtered)
