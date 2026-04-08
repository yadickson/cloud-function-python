from abc import ABC, abstractmethod

from app.domain.model.config_model import ConfigModel


class ConfigMergeMapperInterface(ABC):
    @abstractmethod
    def merge(self, left: ConfigModel, right: ConfigModel) -> ConfigModel:
        pass
