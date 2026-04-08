from injector import inject

from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.use_case.load_config_use_case_interface import LoadConfigUseCaseInterface
from app.domain.validator.config_validator_interface import ConfigValidatorInterface


class LoadConfigUseCase(LoadConfigUseCaseInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        config_repository: ConfigRepositoryInterface,
        config_validator: ConfigValidatorInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.config_repository = config_repository
        self.config_validator = config_validator

    def execute(self) -> None:
        self.logger_repository.running(message="Loading and validating configuration.")
        config = self.config_repository.get_configuration()
        self.config_validator.validate(config=config)
        self.logger_repository.success(message="Configuration is valid.")
