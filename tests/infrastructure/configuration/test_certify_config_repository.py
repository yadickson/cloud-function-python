from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.config_model import ConfigModel
from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.certify_config_repository import CertifyConfigRepository
from app.infrastructure.security.base64_security_interface import Base64SecurityInterface


class TestCertifyConfigRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.config_repository_mock = MagicMock(ConfigRepositoryInterface)
        self.base64_security_mock = MagicMock(Base64SecurityInterface)
        self.config = CertifyConfigRepository(
            config_repository=self.config_repository_mock,
            base64_security=self.base64_security_mock,
        )

    def test_should_check_public_key_value(self) -> None:
        value = self.faker.word()
        processed = self.faker.email()

        security = Autodata.create(ConfigModel)

        security.pgp_public_key = value

        self.config_repository_mock.get_configuration.return_value = security
        self.base64_security_mock.decode.return_value = processed

        response = self.config.get_public_key()

        self.assertEqual(response, processed)

        self.config_repository_mock.get_configuration.assert_called_once_with()
        self.base64_security_mock.decode.assert_called_once_with(content=value)

    def test_should_check_private_key_value(self) -> None:
        security = Autodata.create(ConfigModel)

        value = self.faker.word()
        processed = self.faker.email()

        security.pgp_private_key = value

        self.config_repository_mock.get_configuration.return_value = security
        self.base64_security_mock.decode.return_value = processed

        response = self.config.get_private_key()

        self.assertEqual(response, processed)

        self.config_repository_mock.get_configuration.assert_called_once_with()
        self.base64_security_mock.decode.assert_called_once_with(content=value)

    def test_should_check_password_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()

        security.pgp_password = value

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_password()

        self.assertEqual(response, value)

        self.config_repository_mock.get_configuration.assert_called_once_with()
