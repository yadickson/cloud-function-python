from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.config_model import ConfigModel
from app.infrastructure.configuration.environment_config_repository_interface import EnvironmentConfigRepositoryInterface
from app.infrastructure.configuration.secret_config_repository import SecretConfigRepository


class TestSecretConfigRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.environment_config_repository_mock = MagicMock(EnvironmentConfigRepositoryInterface)
        self.config = SecretConfigRepository(
            environment_config_repository=self.environment_config_repository_mock,
        )

    def test_should_check_secret_key_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        project_id_value = self.faker.word()
        secret_id_value = self.faker.word()
        version_id_value = self.faker.word()

        environment.project_id = project_id_value
        environment.secret_id = secret_id_value
        environment.version_id = version_id_value

        self.environment_config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_secret_id()

        expected = f"projects/{project_id_value}/secrets/{secret_id_value}/versions/{version_id_value}"

        self.assertEqual(response, expected)
        self.environment_config_repository_mock.get_configuration.assert_called_once_with()
