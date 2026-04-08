from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_decompress_mapper_interface import FileDecompressMapperInterface
from app.infrastructure.mapper.file_zip_raw_reader_mapper import FileZipRawReaderMapper
from app.infrastructure.mapper.file_zip_raw_split_mapper_interface import FileZipRawSplitMapperInterface


class TestFileZipRawReaderMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.file_zip_raw_split_mapper = MagicMock(FileZipRawSplitMapperInterface)
        self.decompress_mapper_mock = MagicMock(FileDecompressMapperInterface)

        self.mapper = FileZipRawReaderMapper(
            logger_repository=self.logger_repository_mock,
            file_zip_raw_split_mapper=self.file_zip_raw_split_mapper,
            decompress_mapper=self.decompress_mapper_mock,
        )

    def test_should_check_logger_info_parameters(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)
        contents = [self.faker.binary(length=64) for _ in range(self.faker.random_int(min=10, max=20))]

        file = FileModel(filename=filename, content=content)

        self.file_zip_raw_split_mapper.get_parts.return_value = contents

        self.mapper.read(file)

        call_count = self.logger_repository_mock.info.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.logger_repository_mock.info.call_args_list

        self.assertEqual(call_args_list[0][1], {"message": f"Reading raw {filename} file."})
        self.assertEqual(call_args_list[1][1], {"message": f"Found {len(contents)} files."})

    def test_should_check_slit_content_parameters(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        self.mapper.read(file)

        self.file_zip_raw_split_mapper.get_parts.assert_called_once_with(content=content)

    def test_should_check_decompression_content_parameters(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)
        contents = [self.faker.binary(length=64) for _ in range(4)]

        file = FileModel(filename=filename, content=content)

        self.file_zip_raw_split_mapper.get_parts.return_value = contents

        self.mapper.read(file)

        call_count = self.decompress_mapper_mock.decompress.call_count

        self.assertEqual(4, call_count)

        call_args_list = self.decompress_mapper_mock.decompress.call_args_list

        self.assertEqual(call_args_list[0][1], {"content": contents[0]})
        self.assertEqual(call_args_list[1][1], {"content": contents[1]})
        self.assertEqual(call_args_list[2][1], {"content": contents[2]})
        self.assertEqual(call_args_list[3][1], {"content": contents[3]})

    def test_should_check_response(self) -> None:
        filename = self.faker.word()
        content = self.faker.binary(length=64)
        contents = [self.faker.binary(length=64) for _ in range(2)]

        file = FileModel(filename=filename, content=content)
        files = Autodata.create_many(FileModel, 2)

        self.file_zip_raw_split_mapper.get_parts.return_value = contents
        self.decompress_mapper_mock.decompress.side_effect = files

        response = self.mapper.read(file)

        self.assertListEqual(response, files)
