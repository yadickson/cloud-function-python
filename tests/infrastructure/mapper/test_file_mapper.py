from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_mapper import FileMapper
from app.infrastructure.mapper.file_zip_raw_reader_mapper_interface import FileZipRawReaderMapperInterface
from app.infrastructure.mapper.file_zip_reader_mapper_interface import FileZipReaderMapperInterface
from app.infrastructure.mapper.files_group_mapper_interface import FilesGroupMapperInterface


class TestFileMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.file_zip_reader_mapper_mock = MagicMock(FileZipReaderMapperInterface)
        self.file_zip_raw_reader_mapper_mock = MagicMock(FileZipRawReaderMapperInterface)
        self.files_group_mapper_mock = MagicMock(FilesGroupMapperInterface)

        self.mapper = FileMapper(
            logger_repository=self.logger_repository_mock,
            file_zip_reader_mapper=self.file_zip_reader_mapper_mock,
            file_zip_raw_reader_mapper=self.file_zip_raw_reader_mapper_mock,
            files_group_mapper=self.files_group_mapper_mock,
        )

    def test_should_check_read_parameters(self) -> None:
        file = Autodata.create(FileModel)

        self.mapper.get_files(file=file)

        self.file_zip_reader_mapper_mock.read.assert_called_once_with(file=file)

    def test_should_check_response_reader_file_ok(self) -> None:
        file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 20)
        group_files = Autodata.create_many(FileModel, 40)

        self.file_zip_reader_mapper_mock.read.return_value = files
        self.files_group_mapper_mock.group.return_value = group_files

        response = self.mapper.get_files(file=file)

        self.assertListEqual(response, group_files)
        self.files_group_mapper_mock.group.assert_called_once_with(file=file, files=files)

    def test_should_check_response_reader_file_is_nok(self) -> None:
        file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 20)
        group_files = Autodata.create_many(FileModel, 40)

        exception = Exception("error")

        self.file_zip_reader_mapper_mock.read.side_effect = exception
        self.file_zip_raw_reader_mapper_mock.read.return_value = files
        self.files_group_mapper_mock.group.return_value = group_files

        response = self.mapper.get_files(file=file)

        self.assertListEqual(response, group_files)
        self.file_zip_raw_reader_mapper_mock.read.assert_called_once_with(file=file)
        self.files_group_mapper_mock.group.assert_called_once_with(file=file, files=files)

    def test_should_check_logger_error_parameters(self) -> None:
        file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 20)

        exception = Exception("error")

        self.file_zip_reader_mapper_mock.read.side_effect = exception
        self.file_zip_raw_reader_mapper_mock.read.return_value = files

        self.mapper.get_files(file=file)

        self.logger_repository_mock.error.assert_called_once_with(message="Try to read corrupted file.", cause=exception)

    def test_should_check_reader_parameters(self) -> None:
        file = Autodata.create(FileModel)

        self.mapper.get_files(file=file)

        self.file_zip_reader_mapper_mock.read(file=file)

    def test_should_check_raw_reader_parameters(self) -> None:
        file = Autodata.create(FileModel)

        exception = Exception("error")

        self.file_zip_reader_mapper_mock.read.side_effect = exception

        self.mapper.get_files(file=file)

        self.file_zip_raw_reader_mapper_mock.read(file=file)
