from typing import List

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.files_search_mapper_interface import FilesSearchMapperInterface


class FilesSearchMapper(FilesSearchMapperInterface):
    def search(self, files: List[FileModel], search: list[str]) -> List[FileModel]:
        return [item for item in files if any(find in item.filename for find in list(search))]
