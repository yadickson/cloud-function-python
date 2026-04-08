from dataclasses import replace
from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker
from parameterized import parameterized

from app.domain.model.config_model import ConfigModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.exception.validator_exception import ValidatorException
from app.infrastructure.validator.config_validator import ConfigValidator


class TestConfigValidator(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.validator = ConfigValidator(logger_repository=self.logger_repository_mock)
        self.config_mock = Autodata.create(ConfigModel)

        self.config_mock.source_port = f"{self.faker.random_int(min=20, max=40)}"
        self.config_mock.dest_port = f"{self.faker.random_int(min=20, max=40)}"
        self.config_mock.dest_file_max_registers = f"{self.faker.random_int(min=20, max=40)}"

    def test_should_check_logger_message_when_all_is_ok(self) -> None:
        self.validator.validate(config=self.config_mock)
        self.logger_repository_mock.info.assert_called_once_with(message="Checking configuration variables...")

    @parameterized.expand(
        [
            ("project_id", None),
            ("project_id", ""),
            ("secret_id", None),
            ("secret_id", ""),
            ("source_host", None),
            ("source_host", ""),
            ("source_port", None),
            ("source_port", ""),
            ("source_port", "x"),
            ("source_username", None),
            ("source_username", ""),
            ("source_password", None),
            ("source_password", ""),
            ("source_directory", None),
            ("source_directory", ""),
            ("source_file_filters", None),
            ("source_file_filters", ""),
            ("dest_host", None),
            ("dest_host", ""),
            ("dest_port", None),
            ("dest_port", ""),
            ("dest_port", "x"),
            ("dest_username", None),
            ("dest_username", ""),
            ("dest_password", None),
            ("dest_password", ""),
            ("dest_directory", None),
            ("dest_directory", ""),
            ("dest_file_max_registers", None),
            ("dest_file_max_registers", ""),
            ("pgp_public_key", None),
            ("pgp_public_key", ""),
        ]
    )
    def test_should_check_throws_exception_because_field_is_required(self, key: str, value: str) -> None:
        config = replace(self.config_mock, **{f"{key}": value})

        with self.assertRaises(Exception) as context:
            self.validator.validate(config=config)

        self.assertIsInstance(context.exception, ValidatorException)
        self.logger_repository_mock.error.assert_called_once_with(message=f"{key.upper()} is required.")
        self.assertEqual(str(context.exception), "Configuration validation error.")

    @parameterized.expand(
        [
            ("version_id", None),
            ("version_id", ""),
            ("time_zone", None),
            ("time_zone", ""),
            ("pgp_private_key", None),
            ("pgp_private_key", ""),
            ("pgp_password", None),
            ("pgp_password", ""),
        ]
    )
    def test_should_check_do_not_throw_exception_when_field_is_none(self, key: str, value: str) -> None:
        config = replace(self.config_mock, **{f"{key}": value})

        self.validator.validate(config=config)

        self.logger_repository_mock.error.assert_not_called()
