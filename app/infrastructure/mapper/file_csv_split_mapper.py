from pathlib import Path
from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_csv_group_mapper_interface import FileCsvGroupMapperInterface
from app.infrastructure.mapper.file_csv_key_mapper_interface import FileCsvKeyMapperInterface
from app.infrastructure.mapper.file_csv_split_mapper_interface import FileCsvSplitMapperInterface


class FileCsvSplitMapper(FileCsvSplitMapperInterface):
    @inject
    def __init__(self, csv_group_mapper: FileCsvGroupMapperInterface, csv_key_mapper: FileCsvKeyMapperInterface) -> None:
        self.csv_group_mapper = csv_group_mapper
        self.csv_key_mapper = csv_key_mapper

    def split(self, file: FileModel) -> List[FileModel]:
        filename = Path(file.filename).stem
        extension = Path(file.filename).suffix

        groups = self.csv_group_mapper.group(file=file)

        files = []
        counter = 0

        for group in groups:
            counter += 1
            csv_filename = f"{filename}_{counter}{extension}"
            relations = [self.csv_key_mapper.get_key(line=line) for line in group]
            csv_file = FileModel(filename=csv_filename, content=b"\n".join(group), relations=relations)
            files.append(csv_file)

        return files
