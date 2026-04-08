from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata

from app.domain.model.config_model import ConfigModel
from app.infrastructure.configuration.environment_config_repository_interface import EnvironmentConfigRepositoryInterface
from app.infrastructure.mapper.config_merge_mapper_interface import ConfigMergeMapperInterface
from app.infrastructure.repository.config_repository import ConfigRepository
from app.infrastructure.security.secret_manager_security_interface import SecretManagerSecurityInterface


class TestConfigRepository(TestCase):
    def setUp(self) -> None:
        self.environment_config_repository_mock = MagicMock(EnvironmentConfigRepositoryInterface)
        self.secret_manager_security_mock = MagicMock(SecretManagerSecurityInterface)
        self.config_merge_mapper_mock = MagicMock(ConfigMergeMapperInterface)

        self.config = ConfigRepository(
            environment_config_repository=self.environment_config_repository_mock,
            secret_manager_security=self.secret_manager_security_mock,
            config_merge_mapper=self.config_merge_mapper_mock,
        )

    def test_should_check_order(self) -> None:
        call_order: List[int] = []

        self.environment_config_repository_mock.get_configuration.side_effect = lambda *a, **kw: call_order.append(1)
        self.secret_manager_security_mock.get_configuration.side_effect = lambda *a, **kw: call_order.append(2)
        self.config_merge_mapper_mock.merge.side_effect = lambda *a, **kw: call_order.append(3)

        self.config.get_configuration()

        self.assertSequenceEqual(call_order, [1, 2, 3])

    def test_should_check_get_environment_parameters(self) -> None:
        self.config.get_configuration()

        self.environment_config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_get_secret_parameters(self) -> None:
        self.config.get_configuration()

        self.secret_manager_security_mock.get_configuration.assert_called_once_with()

    def test_should_check_merge_parameters(self) -> None:
        environment = Autodata.create(ConfigModel)
        secrets = Autodata.create(ConfigModel)

        self.environment_config_repository_mock.get_configuration.return_value = environment
        self.secret_manager_security_mock.get_configuration.return_value = secrets

        self.config.get_configuration()

        self.config_merge_mapper_mock.merge.assert_called_once_with(left=environment, right=secrets)

    def test_should_check_response(self) -> None:
        response_mock = Autodata.create(ConfigModel)

        self.config_merge_mapper_mock.merge.return_value = response_mock

        response = self.config.get_configuration()

        self.assertEqual(response, response_mock)
