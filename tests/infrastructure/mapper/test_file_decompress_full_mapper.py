from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.mapper_exception import MapperException
from app.infrastructure.mapper.file_decompress_full_mapper import FileDecompressFullMapper
from app.infrastructure.mapper.file_zip_info_mapper import FileZipInfoMapper


class TestFileDecompressFullMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.zip_file_info_mapper = FileZipInfoMapper()

        self.mapper = FileDecompressFullMapper(
            logger_repository=self.logger_repository_mock,
            zip_file_info_mapper=self.zip_file_info_mapper,
        )

    def test_should_check_filename(self) -> None:
        content = self.faker.zip(uncompressed_size=64, num_files=1, min_file_size=32, compression="deflate")
        filename = self.zip_file_info_mapper.get_filename(content)

        response = self.mapper.decompress_full(content=content)

        self.assertEqual(response.filename, filename)

        call_count = self.logger_repository_mock.info.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.logger_repository_mock.info.call_args_list

        self.assertEqual(call_args_list[1][1], {"message": f"Decompress full filename [{filename}]."})

    def test_should_check_decompress_deflate_content(self) -> None:
        content = self.faker.zip(uncompressed_size=64, num_files=1, min_file_size=32, compression="deflate")
        response = self.mapper.decompress_full(content=content)
        self.assertIsInstance(response, FileModel)

    def test_should_check_logger_info(self) -> None:
        content = self.faker.zip(uncompressed_size=64, num_files=1, min_file_size=32, compression="deflate")

        self.mapper.decompress_full(content=content)

        call_count = self.logger_repository_mock.info.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.logger_repository_mock.info.call_args_list

        self.assertEqual(call_args_list[0][1], {"message": f"Try to decompress full [{len(content)}] bytes."})

    def test_should_check_decompress_gzip_content(self) -> None:
        content = self.faker.zip(uncompressed_size=64, num_files=1, min_file_size=32, compression="gzip")
        response = self.mapper.decompress_full(content=content)
        self.assertIsInstance(response, FileModel)

    def test_should_check_decompress_gz_content(self) -> None:
        content = self.faker.zip(uncompressed_size=64, num_files=1, min_file_size=32, compression="gz")
        response = self.mapper.decompress_full(content=content)
        self.assertIsInstance(response, FileModel)

    def test_should_check_throws_exception_when_try_to_decompress_xz_content(self) -> None:
        content = self.faker.zip(uncompressed_size=64, num_files=1, min_file_size=32, compression="xz")

        with self.assertRaises(Exception) as context:
            self.mapper.decompress_full(content=content)

        self.assertIsInstance(context.exception, MapperException)
        self.assertEqual(context.exception.args[0], "Error to decompress full content.")
        self.assertIsNotNone(context.exception.args[1])

        call_count = self.logger_repository_mock.error.call_count

        self.assertEqual(1, call_count)

        call_args_list = self.logger_repository_mock.error.call_args_list

        self.assertEqual(call_args_list[0][1]["message"], "Error to decompress full content.")
        self.assertIsNotNone(call_args_list[0][1]["cause"])
