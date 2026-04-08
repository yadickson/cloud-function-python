from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_zip_reader_mapper import FileZipReaderMapper


class TestFileZipReaderMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)

        self.mapper = FileZipReaderMapper(logger_repository=self.logger_repository_mock)

    def test_should_check_reader_faker_zip_deflate_file(self) -> None:
        filename = self.faker.word()
        num_files = self.faker.random_int(min=10, max=20)
        content = self.faker.zip(uncompressed_size=64 * num_files, num_files=num_files, min_file_size=32, compression="deflate")

        file = FileModel(filename=filename, content=content)

        response = self.mapper.read(file=file)

        self.assertIsNotNone(response)
        self.assertEqual(num_files, len(response))

        self.assertIsNotNone(response[0].filename)
        self.assertIsNotNone(response[0].content)

        self.assertIsNotNone(response[num_files - 1].filename)
        self.assertIsNotNone(response[num_files - 1].content)

    def test_should_check_logger_info_parameters(self) -> None:
        filename = self.faker.word()
        num_files = self.faker.random_int(min=10, max=20)
        content = self.faker.zip(uncompressed_size=64 * num_files, num_files=num_files, min_file_size=32, compression="deflate")

        file = FileModel(filename=filename, content=content)

        self.mapper.read(file)

        call_count = self.logger_repository_mock.info.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.logger_repository_mock.info.call_args_list

        self.assertEqual(call_args_list[0][1], {"message": f"Reading {filename} file."})
        self.assertEqual(call_args_list[1][1], {"message": f"Found {num_files} files."})
