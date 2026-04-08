from dataclasses import fields
from unittest import TestCase

from faker import Faker

from app.infrastructure.mapper.config_mapper import ConfigMapper


class TestConfigMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.mapper = ConfigMapper()

    def test_should_check_keys(self) -> None:
        configuration: dict = {}
        response = self.mapper.get_configuration(configuration)

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

        configuration = {" ProJect_Id ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.project_id, value)

    def test_should_check_secret_id_value(self) -> None:
        value = self.faker.word()

        configuration = {" Secret_ID ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.secret_id, value)

    def test_should_check_version_id_value(self) -> None:
        value = self.faker.word()

        configuration = {" Version_iD ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.version_id, value)

    def test_should_check_source_host_value(self) -> None:
        value = self.faker.word()

        configuration = {" Source_Host ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_host, value)

    def test_should_check_source_port_value(self) -> None:
        value = self.faker.word()

        configuration = {" Source_POrt ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_port, value)

    def test_should_check_source_port_value_from_int(self) -> None:
        value = self.faker.random_int(min=20, max=40)

        configuration = {" Source_POrt ": value}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_port, f"{value}")

    def test_should_check_source_username_value(self) -> None:
        value = self.faker.word()

        configuration = {" Source_UserName ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_username, value)

    def test_should_check_source_password_value(self) -> None:
        value = self.faker.word()

        configuration = {" Source_passWorD ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_password, value)

    def test_should_check_source_directory_value(self) -> None:
        value = self.faker.word()

        configuration = {" Source_DiRectOry ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_directory, value)

    def test_should_check_source_file_filters_value(self) -> None:
        value = self.faker.word()

        configuration = {" Source_File_FilterS ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.source_file_filters, value)

    def test_should_check_dest_host_value(self) -> None:
        value = self.faker.word()

        configuration = {" dest_Host ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.dest_host, value)

    def test_should_check_dest_port_value(self) -> None:
        value = self.faker.word()

        configuration = {" desT_POrt ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.dest_port, value)

    def test_should_check_dest_username_value(self) -> None:
        value = self.faker.word()

        configuration = {" DesT_UserName ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.dest_username, value)

    def test_should_check_dest_password_value(self) -> None:
        value = self.faker.word()

        configuration = {" deSt_passWorD ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.dest_password, value)

    def test_should_check_dest_directory_value(self) -> None:
        value = self.faker.word()

        configuration = {" dEst_DiRectOry ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.dest_directory, value)

    def test_should_check_dest_file_max_registers_value(self) -> None:
        value = self.faker.word()

        configuration = {" dest_file_Max_registers ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.dest_file_max_registers, value)

    def test_should_check_pgp_public_key_value(self) -> None:
        value = self.faker.word()

        configuration = {" PGP_public_key ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.pgp_public_key, value)

    def test_should_check_pgp_private_key_value(self) -> None:
        value = self.faker.word()

        configuration = {" PGP_Private_key ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.pgp_private_key, value)

    def test_should_check_pgp_password_value(self) -> None:
        value = self.faker.word()

        configuration = {" PGP_Password ": f" {value} "}

        response = self.mapper.get_configuration(configuration)

        self.assertEqual(response.pgp_password, value)
