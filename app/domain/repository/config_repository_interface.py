from abc import ABC, abstractmethod

from app.domain.model.config_model import ConfigModel


class ConfigRepositoryInterface(ABC):
    @abstractmethod
    def get_configuration(self) -> ConfigModel:
        pass
