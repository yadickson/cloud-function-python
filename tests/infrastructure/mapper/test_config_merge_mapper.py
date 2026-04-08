from dataclasses import fields
from unittest import TestCase

from autofaker import Autodata
from faker import Faker
from parameterized import parameterized

from app.domain.model.config_model import ConfigModel
from app.infrastructure.mapper.config_merge_mapper import ConfigMergeMapper


class TestConfigMergeMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.mapper = ConfigMergeMapper()

    def test_should_check_empty_merge(self) -> None:
        left = Autodata.create(ConfigModel)
        right = Autodata.create(ConfigModel)

        left.version_id = None
        right.version_id = None

        response = self.mapper.merge(left=left, right=right)

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

    @parameterized.expand(
        [
            None,
            "",
        ]
    )
    def test_should_check_time_zone_value_from_right(self, right_value: str) -> None:
        left = Autodata.create(ConfigModel)
        right = Autodata.create(ConfigModel)

        value = self.faker.word()

        left.time_zone = value
        right.time_zone = right_value

        response = self.mapper.merge(left=left, right=right)

        self.assertEqual(response.time_zone, value)

    @parameterized.expand(
        [
            None,
            "",
            ".",
            "x",
        ]
    )
    def test_should_check_time_zone_value_from_left(self, left_value: str) -> None:
        left = Autodata.create(ConfigModel)
        right = Autodata.create(ConfigModel)

        value = self.faker.word()

        left.time_zone = left_value
        right.time_zone = value

        response = self.mapper.merge(left=left, right=right)

        self.assertEqual(response.time_zone, value)
