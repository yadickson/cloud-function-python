import json

from dacite import Config, from_dict
from google.cloud import secretmanager
from injector import inject

from app.domain.model.config_model import ConfigModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.secret_config_repository_interface import SecretConfigRepositoryInterface
from app.infrastructure.constants.encodings_enum import EncodingsEnum
from app.infrastructure.mapper.config_mapper_interface import ConfigMapperInterface
from app.infrastructure.security.secret_manager_security_interface import SecretManagerSecurityInterface


class SecretManagerSecurity(SecretManagerSecurityInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        secret_config_repository: SecretConfigRepositoryInterface,
        config_mapper: ConfigMapperInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.secret_config_repository = secret_config_repository
        self.config_mapper = config_mapper

    def get_configuration(self) -> ConfigModel:
        try:
            secret_id = self.secret_config_repository.get_secret_id()
            client = secretmanager.SecretManagerServiceClient()
            json_secret = client.access_secret_version(request={"name": secret_id})
            json_payload = json_secret.payload.data.decode(EncodingsEnum.UTF8)
            json_config = json.loads(json_payload)
            return self.config_mapper.get_configuration(config=json_config)
        except Exception as exception:
            self.logger_repository.warn(message="Error to get secret id.", cause=exception)
            return from_dict(data_class=ConfigModel, data={}, config=Config(allow_missing_fields_as_none=True))
