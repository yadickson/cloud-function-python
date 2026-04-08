import os
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.config_model import ConfigModel
from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.destination_config_repository import DestinationConfigRepository
from app.infrastructure.security.base64_security_interface import Base64SecurityInterface


class TestDestinationConfigRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.config_repository_mock = MagicMock(ConfigRepositoryInterface)
        self.base64_security_mock = MagicMock(Base64SecurityInterface)
        self.config = DestinationConfigRepository(
            config_repository=self.config_repository_mock,
            base64_security=self.base64_security_mock,
        )

    def test_should_check_host_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()

        security.dest_host = value

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_host()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_port_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.random_int(min=10, max=40)

        security.dest_port = f"{value}"

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_port()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_username_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()

        security.dest_username = value

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_username()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_password_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()
        secret = self.faker.word()

        security.dest_password = value

        self.config_repository_mock.get_configuration.return_value = security
        self.base64_security_mock.decode.return_value = secret

        response = self.config.get_password()

        self.assertEqual(response, secret)
        self.config_repository_mock.get_configuration.assert_called_once_with()
        self.base64_security_mock.decode.assert_called_once_with(value)

    def test_should_check_directory_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        value = self.faker.word()

        environment.dest_directory = value

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_destination_directory()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_max_register_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        value = self.faker.random_int(min=20, max=40)

        environment.dest_file_max_registers = f"{value}"

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_destination_file_max_registers()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_full_filename_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        directory = self.faker.word()
        filename = self.faker.word()

        environment.dest_directory = directory

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_destination_full_filename(filename=filename)

        self.assertEqual(response, os.path.join(directory, filename))
        self.config_repository_mock.get_configuration.assert_called_once_with()
