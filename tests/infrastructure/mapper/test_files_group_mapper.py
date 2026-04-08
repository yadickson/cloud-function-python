from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.files_compress_mapper_interface import FilesCompressMapperInterface
from app.infrastructure.mapper.files_csv_split_mapper_interface import FilesCsvSplitMapperInterface
from app.infrastructure.mapper.files_group_mapper import FilesGroupMapper
from app.infrastructure.mapper.files_search_mapper_interface import FilesSearchMapperInterface


class TestFilesGroupMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.files_search_mapper_mock = MagicMock(FilesSearchMapperInterface)
        self.files_csv_split_mapper_mock = MagicMock(FilesCsvSplitMapperInterface)
        self.files_compress_mapper_mock = MagicMock(FilesCompressMapperInterface)
        self.mapper = FilesGroupMapper(
            files_search_mapper=self.files_search_mapper_mock,
            files_csv_split_mapper=self.files_csv_split_mapper_mock,
            files_compress_mapper=self.files_compress_mapper_mock,
        )

    def test_should_check_files_search_mapper_parameters(self) -> None:
        file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 10)

        self.mapper.group(file=file, files=files)

        call_count = self.files_search_mapper_mock.search.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.files_search_mapper_mock.search.call_args_list

        self.assertEqual(call_args_list[0][1], {"files": files, "search": [".csv"]})
        self.assertEqual(call_args_list[1][1], {"files": files, "search": [".pdf"]})

    def test_should_check_files_csv_split_mapper_parameters(self) -> None:
        file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 10)
        csv_filtered = Autodata.create_many(FileModel, 6)
        pdf_filtered = Autodata.create_many(FileModel, 4)

        self.files_search_mapper_mock.search.side_effect = [csv_filtered, pdf_filtered]

        self.mapper.group(file=file, files=files)

        self.files_csv_split_mapper_mock.split.assert_called_once_with(files=csv_filtered)

    def test_should_check_file_compress_mapper_parameters(self) -> None:
        file = Autodata.create(FileModel)
        files = Autodata.create_many(FileModel, 10)
        csv_filtered = Autodata.create_many(FileModel, 6)
        pdf_filtered = Autodata.create_many(FileModel, 4)

        csv_split_files = Autodata.create_many(FileModel, 2)

        self.files_search_mapper_mock.search.side_effect = [csv_filtered, pdf_filtered]
        self.files_csv_split_mapper_mock.split.return_value = csv_split_files

        self.mapper.group(file=file, files=files)

        call_count = self.files_compress_mapper_mock.compress.call_count

        self.assertEqual(2, call_count)

        call_args_list = self.files_compress_mapper_mock.compress.call_args_list

        self.assertEqual(call_args_list[0][1], {"file": file, "csv_file": csv_split_files[0], "files": pdf_filtered})
        self.assertEqual(call_args_list[1][1], {"file": file, "csv_file": csv_split_files[1], "files": pdf_filtered})
