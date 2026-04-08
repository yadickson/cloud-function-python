from unittest import TestCase
from unittest.mock import MagicMock, patch

from autofaker import Autodata
from faker import Faker
from google.cloud import secretmanager
from google.cloud.secretmanager_v1.types import SecretPayload
from google.cloud.secretmanager_v1.types.service import AccessSecretVersionResponse

from app.domain.model.config_model import ConfigModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.secret_config_repository_interface import SecretConfigRepositoryInterface
from app.infrastructure.constants.encodings_enum import EncodingsEnum
from app.infrastructure.mapper.config_mapper_interface import ConfigMapperInterface
from app.infrastructure.security.secret_manager_security import SecretManagerSecurity


class TestSecretManagerSecurity(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.secret_config_repository_mock = MagicMock(SecretConfigRepositoryInterface)
        self.config_mapper_mock = MagicMock(ConfigMapperInterface)
        self.client_mock = MagicMock(secretmanager.SecretManagerServiceClient)

        self.security = SecretManagerSecurity(
            logger_repository=self.logger_repository_mock,
            secret_config_repository=self.secret_config_repository_mock,
            config_mapper=self.config_mapper_mock,
        )

    def test_should_check_get_data_config(self) -> None:
        data = self.faker.word()

        secret_response = Autodata.create(AccessSecretVersionResponse)
        payload = Autodata.create(SecretPayload)
        payload.data = data.encode(EncodingsEnum.UTF8)

        secret_response.payload = payload

        self.client_mock.access_secret_version.return_value = secret_response

        with patch("google.cloud.secretmanager.SecretManagerServiceClient") as client:
            with patch("json.loads") as json:
                client.return_value = self.client_mock
                self.security.get_configuration()
                json.assert_called_once_with(data)

    def test_should_check_get_json_config(self) -> None:
        secret_id = self.faker.word()
        config_dict = self.faker.pydict(nb_elements=2, value_types=[str])

        self.secret_config_repository_mock.get_secret_id.return_value = secret_id

        with patch("google.cloud.secretmanager.SecretManagerServiceClient") as client:
            with patch("json.loads") as json:
                client.return_value = self.client_mock
                json.return_value = config_dict

                self.security.get_configuration()

        self.client_mock.access_secret_version.assert_called_once_with(request={"name": secret_id})
        self.config_mapper_mock.get_configuration.assert_called_once_with(config=config_dict)

    def test_should_check_response(self) -> None:
        config = Autodata.create(ConfigModel)

        self.config_mapper_mock.get_configuration.return_value = config

        with patch("google.cloud.secretmanager.SecretManagerServiceClient"):
            with patch("json.loads"):
                response = self.security.get_configuration()

        self.assertEqual(response, config)

    def test_should_check_empty_config_when_connection_fail(self) -> None:
        secret_id = self.faker.word()
        exception = Exception("error")

        self.secret_config_repository_mock.get_secret_id.return_value = secret_id

        with patch("google.cloud.secretmanager.SecretManagerServiceClient") as client:
            with patch("json.loads"):
                client.side_effect = exception
                response = self.security.get_configuration()

        self.assertIsInstance(response, ConfigModel)
        self.logger_repository_mock.warn.assert_called_once_with(message="Error to get secret id.", cause=exception)
