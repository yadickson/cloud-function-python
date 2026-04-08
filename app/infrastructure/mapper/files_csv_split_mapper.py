from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_csv_split_mapper_interface import FileCsvSplitMapperInterface
from app.infrastructure.mapper.files_csv_split_mapper_interface import FilesCsvSplitMapperInterface


class FilesCsvSplitMapper(FilesCsvSplitMapperInterface):
    @inject
    def __init__(self, file_csv_split_mapper: FileCsvSplitMapperInterface) -> None:
        self.file_csv_split_mapper = file_csv_split_mapper

    def split(self, files: List[FileModel]) -> List[FileModel]:
        file_lists = [self.file_csv_split_mapper.split(file=file) for file in files]
        return [file for sublist in file_lists for file in sublist]
