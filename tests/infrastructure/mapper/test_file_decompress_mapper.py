from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_decompress_full_mapper_interface import FileDecompressFullMapperInterface
from app.infrastructure.mapper.file_decompress_mapper import FileDecompressMapper
from app.infrastructure.mapper.file_decompress_raw_mapper_interface import FileDecompressRawMapperInterface


class TestFileDecompressMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.decompress_full_mapper_mock = MagicMock(FileDecompressFullMapperInterface)
        self.decompress_raw_mapper_mock = MagicMock(FileDecompressRawMapperInterface)
        self.mapper = FileDecompressMapper(
            logger_repository=self.logger_repository_mock,
            decompress_full_mapper=self.decompress_full_mapper_mock,
            decompress_raw_mapper=self.decompress_raw_mapper_mock,
        )

    def test_should_check_decompress_full_content(self) -> None:
        content = self.faker.binary(length=64)
        file = Autodata.create(FileModel)

        self.decompress_full_mapper_mock.decompress_full.return_value = file

        response = self.mapper.decompress(content=content)

        self.assertEqual(response, file)
        self.decompress_full_mapper_mock.decompress_full.assert_called_once_with(content=content)

    def test_should_check_decompress_raw_content_when_full_fail(self) -> None:
        content = self.faker.binary(length=64)
        file = Autodata.create(FileModel)
        exception = Exception("error")

        self.decompress_full_mapper_mock.decompress_full.side_effect = exception
        self.decompress_raw_mapper_mock.decompress_raw.return_value = file

        response = self.mapper.decompress(content=content)

        self.assertEqual(response, file)
        self.logger_repository_mock.error.assert_called_once_with(message="Error to decompress content.", cause=exception)
        self.decompress_raw_mapper_mock.decompress_raw.assert_called_once_with(content=content)
