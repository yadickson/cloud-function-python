from abc import ABC, abstractmethod

from app.domain.model.config_model import ConfigModel


class ConfigValidatorInterface(ABC):
    @abstractmethod
    def validate(self, config: ConfigModel) -> None:
        pass
