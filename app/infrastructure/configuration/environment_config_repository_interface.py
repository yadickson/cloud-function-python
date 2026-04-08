from abc import ABC, abstractmethod

from app.domain.model.config_model import ConfigModel


class EnvironmentConfigRepositoryInterface(ABC):
    @abstractmethod
    def get_configuration(self) -> ConfigModel:
        pass
