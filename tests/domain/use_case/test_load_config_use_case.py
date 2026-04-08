from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.config_model import ConfigModel
from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.use_case.load_config_use_case import LoadConfigUseCase
from app.domain.validator.config_validator_interface import ConfigValidatorInterface


class TestLoadConfigUseCase(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.config_repository_mock = MagicMock(ConfigRepositoryInterface)
        self.config_validator_mock = MagicMock(ConfigValidatorInterface)

        self.use_case = LoadConfigUseCase(
            logger_repository=self.logger_repository_mock,
            config_repository=self.config_repository_mock,
            config_validator=self.config_validator_mock,
        )

    def test_should_check_order(self) -> None:
        call_order: List[int] = []

        self.logger_repository_mock.running.side_effect = lambda *a, **kw: call_order.append(1)
        self.config_repository_mock.get_configuration.side_effect = lambda *a, **kw: call_order.append(2)
        self.config_validator_mock.validate.side_effect = lambda *a, **kw: call_order.append(3)
        self.logger_repository_mock.success.side_effect = lambda *a, **kw: call_order.append(4)

        self.use_case.execute()

        self.assertSequenceEqual(call_order, [1, 2, 3, 4])

    def test_should_check_running_logger_parameters(self) -> None:
        self.use_case.execute()

        self.logger_repository_mock.running.assert_called_once_with(message="Loading and validating configuration.")

    def test_should_check_get_configuration_parameters(self) -> None:
        self.use_case.execute()

        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_validator_parameters(self) -> None:
        config_mock = Autodata.create(ConfigModel)

        self.config_repository_mock.get_configuration.return_value = config_mock

        self.use_case.execute()

        self.config_validator_mock.validate.assert_called_once_with(config=config_mock)

    def test_should_check_success_logger_parameters(self) -> None:
        self.use_case.execute()
        self.logger_repository_mock.success.assert_called_once_with(message="Configuration is valid.")
