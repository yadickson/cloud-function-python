from abc import ABC, abstractmethod


class TimeZoneConfigRepositoryInterface(ABC):
    @abstractmethod
    def get_time_zone(self) -> str:
        pass
