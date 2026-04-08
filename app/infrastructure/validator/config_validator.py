from dataclasses import asdict

from injector import inject
from marshmallow import ValidationError

from app.domain.model.config_model import ConfigModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.validator.config_validator_interface import ConfigValidatorInterface
from app.infrastructure.exception.validator_exception import ValidatorException
from app.infrastructure.validator.config_schema import ConfigSchema


class ConfigValidator(ConfigValidatorInterface):
    @inject
    def __init__(self, logger_repository: LoggerRepositoryInterface) -> None:
        self.logger_repository = logger_repository

    def validate(self, config: ConfigModel) -> None:
        self.logger_repository.info(message="Checking configuration variables...")

        try:
            ConfigSchema().load(asdict(config))
        except ValidationError as exception:
            [self.logger_repository.error(message=message[0]) for message in exception.messages_dict.values()]
            raise ValidatorException("Configuration validation error.")
