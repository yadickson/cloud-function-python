import os
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.config_model import ConfigModel
from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.source_config_repository import SourceConfigRepository


class TestSourceConfigRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.config_repository_mock = MagicMock(ConfigRepositoryInterface)
        self.config = SourceConfigRepository(
            config_repository=self.config_repository_mock,
        )

    def test_should_check_host_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()

        security.source_host = value

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_host()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_port_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.random_int(min=10, max=40)

        security.source_port = f"{value}"

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_port()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_username_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()

        security.source_username = value

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_username()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_password_value(self) -> None:
        security = Autodata.create(ConfigModel)
        value = self.faker.word()

        security.source_password = value

        self.config_repository_mock.get_configuration.return_value = security

        response = self.config.get_password()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_directory_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        value = self.faker.word()

        environment.source_directory = value

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_source_directory()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_file_filters_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        value_one = self.faker.word()
        value_two = self.faker.word()

        environment.source_file_filters = f"{value_one}|{value_two}"

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_source_file_filters()

        self.assertListEqual(response, [value_one, value_two])
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_full_filename_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        directory = self.faker.word()
        filename = self.faker.word()

        environment.source_directory = directory

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_source_full_filename(filename=filename)

        self.assertEqual(response, os.path.join(directory, filename))
        self.config_repository_mock.get_configuration.assert_called_once_with()
