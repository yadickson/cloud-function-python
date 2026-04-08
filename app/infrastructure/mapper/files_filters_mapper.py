import datetime
from typing import List

import pytz
from injector import inject

from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.configuration.timezone_config_repository_interface import TimeZoneConfigRepositoryInterface
from app.infrastructure.mapper.files_filters_mapper_interface import FilesFiltersMapperInterface


class FilesFiltersMapper(FilesFiltersMapperInterface):
    @inject
    def __init__(
        self,
        source_config: SourceConfigRepositoryInterface,
        time_zone_config: TimeZoneConfigRepositoryInterface,
    ) -> None:
        self.source_config = source_config
        self.time_zone_config = time_zone_config

    def get_files(self) -> List[str]:
        files = self.source_config.get_source_file_filters()
        time_zone = self.time_zone_config.get_time_zone()
        filter_placeholder = "(date)"
        date_filter = datetime.datetime.now(tz=pytz.timezone(time_zone)).strftime("%Y%m%d")
        return [f"{file.replace(filter_placeholder, date_filter)}" for file in files]
