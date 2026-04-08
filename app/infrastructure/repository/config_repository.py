from injector import inject

from app.domain.model.config_model import ConfigModel
from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.environment_config_repository_interface import EnvironmentConfigRepositoryInterface
from app.infrastructure.mapper.config_merge_mapper_interface import ConfigMergeMapperInterface
from app.infrastructure.security.secret_manager_security_interface import SecretManagerSecurityInterface


class ConfigRepository(ConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        environment_config_repository: EnvironmentConfigRepositoryInterface,
        secret_manager_security: SecretManagerSecurityInterface,
        config_merge_mapper: ConfigMergeMapperInterface,
    ) -> None:
        self.environment_config_repository = environment_config_repository
        self.secret_manager_security = secret_manager_security
        self.config_merge_mapper = config_merge_mapper

    def get_configuration(self) -> ConfigModel:
        environment = self.environment_config_repository.get_configuration()
        secrets = self.secret_manager_security.get_configuration()
        return self.config_merge_mapper.merge(left=environment, right=secrets)
