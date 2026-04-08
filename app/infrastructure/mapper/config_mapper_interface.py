from abc import ABC, abstractmethod

from app.domain.model.config_model import ConfigModel


class ConfigMapperInterface(ABC):
    @abstractmethod
    def get_configuration(self, config: dict) -> ConfigModel:
        pass
