from injector import inject

from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.timezone_config_repository_interface import TimeZoneConfigRepositoryInterface


class TimeZoneConfigRepository(TimeZoneConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        config_repository: ConfigRepositoryInterface,
    ) -> None:
        self.config_repository = config_repository

    def get_time_zone(self) -> str:
        value = self.config_repository.get_configuration().time_zone
        return value if value else "America/Santiago"
