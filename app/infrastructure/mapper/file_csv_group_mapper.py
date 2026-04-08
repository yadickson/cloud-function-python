import io
from typing import List

from injector import inject

from app.domain.model.file_model import FileModel
from app.infrastructure.configuration.destination_config_repository_interface import DestinationConfigRepositoryInterface
from app.infrastructure.mapper.file_csv_group_mapper_interface import FileCsvGroupMapperInterface


class FileCsvGroupMapper(FileCsvGroupMapperInterface):
    @inject
    def __init__(self, config: DestinationConfigRepositoryInterface) -> None:
        self.config = config

    def group(self, file: FileModel) -> List[List[bytes]]:
        with io.BytesIO(file.content) as buffer:
            lines = buffer.getvalue().splitlines()

        count = self.config.get_destination_file_max_registers()

        return [lines[i : i + count] for i in range(0, len(lines), count)]
