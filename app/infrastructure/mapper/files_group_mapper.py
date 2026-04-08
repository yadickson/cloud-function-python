from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.files_compress_mapper_interface import FilesCompressMapperInterface
from app.infrastructure.mapper.files_csv_split_mapper_interface import FilesCsvSplitMapperInterface
from app.infrastructure.mapper.files_group_mapper_interface import FilesGroupMapperInterface
from app.infrastructure.mapper.files_search_mapper_interface import FilesSearchMapperInterface


class FilesGroupMapper(FilesGroupMapperInterface):
    @inject
    def __init__(
        self,
        files_search_mapper: FilesSearchMapperInterface,
        files_csv_split_mapper: FilesCsvSplitMapperInterface,
        files_compress_mapper: FilesCompressMapperInterface,
    ) -> None:
        self.files_search_mapper = files_search_mapper
        self.files_csv_split_mapper = files_csv_split_mapper
        self.files_compress_mapper = files_compress_mapper

    def group(self, file: FileModel, files: List[FileModel]) -> List[FileModel]:
        csv_filtered = self.files_search_mapper.search(files=files, search=[".csv"])
        pdf_filtered = self.files_search_mapper.search(files=files, search=[".pdf"])
        csv_split_files = self.files_csv_split_mapper.split(files=csv_filtered)
        return [self.files_compress_mapper.compress(file=file, csv_file=csv_file, files=pdf_filtered) for csv_file in csv_split_files]
