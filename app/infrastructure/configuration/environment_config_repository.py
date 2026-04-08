import os

from injector import inject

from app.domain.model.config_model import ConfigModel
from app.infrastructure.configuration.environment_config_repository_interface import EnvironmentConfigRepositoryInterface
from app.infrastructure.mapper.config_mapper_interface import ConfigMapperInterface


class EnvironmentConfigRepository(EnvironmentConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        config_mapper: ConfigMapperInterface,
    ) -> None:
        self.config_mapper = config_mapper

    def get_configuration(self) -> ConfigModel:
        return self.config_mapper.get_configuration(dict(os.environ))
