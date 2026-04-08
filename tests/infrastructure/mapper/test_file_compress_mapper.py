from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_compress_mapper import FileCompressMapper
from app.infrastructure.mapper.file_zip_reader_mapper import FileZipReaderMapper


class TestFileCompressMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.mapper = FileCompressMapper()
        self.reader = FileZipReaderMapper(self.logger_repository_mock)

    def test_should_check_compress_one_file(self) -> None:
        filename = self.faker.word()

        internal_filename = self.faker.word()
        internal_content = self.faker.binary(length=64)

        files = [FileModel(filename=internal_filename, content=internal_content)]

        response = self.mapper.compress(filename=filename, files=files)

        self.assertIsInstance(response, FileModel)
        self.assertEqual(response.filename, filename)
        self.assertIsNotNone(response.content)

    def test_should_check_compress_alot_files(self) -> None:
        filename = self.faker.word()

        files = Autodata.create_many(FileModel, 20)

        response = self.mapper.compress(filename=filename, files=files)

        self.assertIsInstance(response, FileModel)
        self.assertEqual(response.filename, filename)
        self.assertIsNotNone(response.content)

    def test_should_check_compress_and_decompress_file(self) -> None:
        filename = self.faker.word()

        internal_filename = self.faker.word()
        internal_content = self.faker.binary(length=10000002)

        files = [FileModel(filename=internal_filename, content=internal_content)]

        response = self.mapper.compress(filename=filename, files=files)

        self.assertIsNotNone(response)

        decompress_files = self.reader.read(response)

        self.assertIsNotNone(decompress_files)
        self.assertEqual(len(decompress_files), 1)
        self.assertEqual(decompress_files[0].filename, internal_filename)
