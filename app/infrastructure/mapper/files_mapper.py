from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_mapper_interface import FileMapperInterface
from app.infrastructure.mapper.files_mapper_interface import FilesMapperInterface


class FilesMapper(FilesMapperInterface):
    @inject
    def __init__(self, file_mapper: FileMapperInterface) -> None:
        self.file_mapper = file_mapper

    def get_files(self, files: List[FileModel]) -> List[FileModel]:
        file_lists = [self.file_mapper.get_files(file=file) for file in files]
        return [file for sublist in file_lists for file in sublist]
