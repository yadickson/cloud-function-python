from injector import inject

from app.infrastructure.configuration.environment_config_repository_interface import EnvironmentConfigRepositoryInterface
from app.infrastructure.configuration.secret_config_repository_interface import SecretConfigRepositoryInterface


class SecretConfigRepository(SecretConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        environment_config_repository: EnvironmentConfigRepositoryInterface,
    ) -> None:
        self.environment_config_repository = environment_config_repository

    def get_secret_id(self) -> str:
        environment = self.environment_config_repository.get_configuration()
        return f"projects/{environment.project_id}/secrets/{environment.secret_id}/versions/{environment.version_id}"
