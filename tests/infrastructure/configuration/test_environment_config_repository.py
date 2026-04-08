import os
from dataclasses import fields
from unittest import TestCase

from faker import Faker

from app.infrastructure.configuration.environment_config_repository import EnvironmentConfigRepository
from app.infrastructure.mapper.config_mapper import ConfigMapper


class TestEnvironmentConfigRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.config = EnvironmentConfigRepository(config_mapper=ConfigMapper())

    def test_should_check_keys(self) -> None:
        response = self.config.get_configuration()

        all_keys = [file.name for file in fields(response)]

        self.assertListEqual(
            all_keys,
            [
                "project_id",
                "secret_id",
                "version_id",
                "time_zone",
                "source_host",
                "source_port",
                "source_username",
                "source_password",
                "source_directory",
                "source_file_filters",
                "dest_host",
                "dest_port",
                "dest_username",
                "dest_password",
                "dest_directory",
                "dest_file_max_registers",
                "pgp_public_key",
                "pgp_private_key",
                "pgp_password",
            ],
        )

    def test_should_check_project_id_value(self) -> None:
        value = self.faker.word()
        os.environ["PROJECT_ID"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.project_id, value)

    def test_should_check_secret_id_value(self) -> None:
        value = self.faker.word()
        os.environ["SECRET_ID"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.secret_id, value)

    def test_should_check_version_id_value(self) -> None:
        value = self.faker.word()
        os.environ["VERSION_ID"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.version_id, value)

    def test_should_check_time_zone_value(self) -> None:
        value = self.faker.word()
        os.environ["TIME_ZONE"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.time_zone, value)

    def test_should_check_source_host_value(self) -> None:
        value = self.faker.word()
        os.environ["SOURCE_HOST"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.source_host, value)

    def test_should_check_source_port_value(self) -> None:
        value = self.faker.word()
        os.environ["SOURCE_PORT"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.source_port, value)

    def test_should_check_source_username_value(self) -> None:
        value = self.faker.word()
        os.environ["SOURCE_USERNAME"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.source_username, value)

    def test_should_check_source_password_value(self) -> None:
        value = self.faker.word()
        os.environ["SOURCE_PASSWORD"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.source_password, value)

    def test_should_check_source_directory_value(self) -> None:
        value = self.faker.word()
        os.environ["SOURCE_DIRECTORY"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.source_directory, value)

    def test_should_check_source_file_filters_value(self) -> None:
        value = self.faker.word()
        os.environ["SOURCE_FILE_FILTERS"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.source_file_filters, value)

    def test_should_check_dest_host_value(self) -> None:
        value = self.faker.word()
        os.environ["DEST_HOST"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.dest_host, value)

    def test_should_check_dest_port_value(self) -> None:
        value = self.faker.word()
        os.environ["DEST_PORT"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.dest_port, value)

    def test_should_check_dest_username_value(self) -> None:
        value = self.faker.word()
        os.environ["DEST_USERNAME"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.dest_username, value)

    def test_should_check_dest_password_value(self) -> None:
        value = self.faker.word()
        os.environ["DEST_PASSWORD"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.dest_password, value)

    def test_should_check_directory_value(self) -> None:
        value = self.faker.word()
        os.environ["DEST_DIRECTORY"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.dest_directory, value)

    def test_should_check_max_register_value(self) -> None:
        value = self.faker.word()
        os.environ["DEST_FILE_MAX_REGISTERS"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.dest_file_max_registers, value)

    def test_should_check_pgp_public_key_value(self) -> None:
        value = self.faker.word()
        os.environ["PGP_PUBLIC_KEY"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.pgp_public_key, value)

    def test_should_check_pgp_private_key_value(self) -> None:
        value = self.faker.word()
        os.environ["PGP_PRIVATE_KEY"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.pgp_private_key, value)

    def test_should_check_pgp_password_value(self) -> None:
        value = self.faker.word()
        os.environ["PGP_PASSWORD"] = value

        response = self.config.get_configuration()

        self.assertEqual(response.pgp_password, value)
