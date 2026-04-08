import re
from typing import List

from injector import inject

from app.infrastructure.mapper.files_filtered_mapper_interface import FilesFilteredMapperInterface
from app.infrastructure.mapper.files_filters_mapper_interface import FilesFiltersMapperInterface


class FilesFilteredMapper(FilesFilteredMapperInterface):
    @inject
    def __init__(
        self,
        files_filters_mapper: FilesFiltersMapperInterface,
    ) -> None:
        self.files_filters_mapper = files_filters_mapper

    def filter(self, files: List[str]) -> List[str]:
        files_filters = self.files_filters_mapper.get_files()
        return [file for file in files if any(re.search(search, file, re.IGNORECASE) for search in files_filters)]
