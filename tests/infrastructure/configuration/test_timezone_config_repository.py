from unittest import TestCase
from unittest.mock import MagicMock

from autofaker import Autodata
from faker import Faker

from app.domain.model.config_model import ConfigModel
from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.timezone_config_repository import TimeZoneConfigRepository


class TestTimeZoneConfigRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.config_repository_mock = MagicMock(ConfigRepositoryInterface)
        self.config = TimeZoneConfigRepository(
            config_repository=self.config_repository_mock,
        )

    def test_should_check_time_zone_value(self) -> None:
        environment = Autodata.create(ConfigModel)
        value = self.faker.word()

        environment.time_zone = value

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_time_zone()

        self.assertEqual(response, value)
        self.config_repository_mock.get_configuration.assert_called_once_with()

    def test_should_check_time_zone_by_default_value(self) -> None:
        environment = Autodata.create(ConfigModel)

        environment.time_zone = None

        self.config_repository_mock.get_configuration.return_value = environment

        response = self.config.get_time_zone()

        self.assertEqual(response, "America/Santiago")
        self.config_repository_mock.get_configuration.assert_called_once_with()
