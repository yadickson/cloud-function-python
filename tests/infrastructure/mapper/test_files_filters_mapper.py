import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytz
from faker import Faker

from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.configuration.timezone_config_repository_interface import TimeZoneConfigRepositoryInterface
from app.infrastructure.mapper.files_filters_mapper import FilesFiltersMapper


class TestFilesFiltersMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.source_config_mock = MagicMock(SourceConfigRepositoryInterface)
        self.time_zone_config_mock = MagicMock(TimeZoneConfigRepositoryInterface)
        self.datetime_now_mock = MagicMock(datetime.datetime)

        self.mapper = FilesFiltersMapper(
            source_config=self.source_config_mock,
            time_zone_config=self.time_zone_config_mock,
        )

    def test_should_check_config_files_parameters(self) -> None:
        with patch("pytz.timezone"):
            with patch("datetime.datetime"):
                self.mapper.get_files()

        self.source_config_mock.get_source_file_filters.assert_called_once_with()

    def test_should_check_time_zone_parameters(self) -> None:
        with patch("pytz.timezone"):
            with patch("datetime.datetime"):
                self.mapper.get_files()

        self.time_zone_config_mock.get_time_zone.assert_called_once_with()

    def test_should_check_pytz_timezone_parameters(self) -> None:
        timezone = self.faker.word()

        self.time_zone_config_mock.get_time_zone.return_value = timezone

        with patch("pytz.timezone") as py_timezone:
            with patch("datetime.datetime"):
                self.mapper.get_files()

        py_timezone.assert_called_once_with(timezone)

    def test_should_check_datetime_now_parameters(self) -> None:
        timezone = MagicMock(pytz.UTC)

        self.time_zone_config_mock.get_time_zone.return_value = timezone

        with patch("pytz.timezone") as py_timezone:
            py_timezone.return_value = timezone
            with patch("datetime.datetime") as date_time:
                self.mapper.get_files()

        date_time.now.assert_called_once_with(tz=timezone)

    def test_should_check_empty_response(self) -> None:
        with patch("pytz.timezone"):
            with patch("datetime.datetime"):
                response = self.mapper.get_files()

        self.assertListEqual(response, [])

    def test_should_check_str_time_parameters(self) -> None:
        with patch("pytz.timezone"):
            with patch("datetime.datetime") as date_time:
                date_time.now.return_value = self.datetime_now_mock
                self.mapper.get_files()

        self.datetime_now_mock.strftime.assert_called_once_with("%Y%m%d")

    def test_should_check_response(self) -> None:
        file_one = self.faker.word()
        file_two = self.faker.word()
        now_filter = self.faker.word()

        self.source_config_mock.get_source_file_filters.return_value = [file_one, file_two]
        self.datetime_now_mock.strftime.return_value = now_filter

        with patch("pytz.timezone"):
            with patch("datetime.datetime") as date_time:
                date_time.now.return_value = self.datetime_now_mock
                response = self.mapper.get_files()

        self.assertListEqual(response, [file_one, file_two])

    def test_should_check_response_mix_date(self) -> None:
        file_one = self.faker.word()
        file_two = self.faker.word()
        now_filter = self.faker.word()

        self.source_config_mock.get_source_file_filters.return_value = [file_one, f"{file_two}(date)"]
        self.datetime_now_mock.strftime.return_value = now_filter

        with patch("pytz.timezone"):
            with patch("datetime.datetime") as date_time:
                date_time.now.return_value = self.datetime_now_mock
                response = self.mapper.get_files()

        self.assertListEqual(response, [file_one, f"{file_two}{now_filter}"])

    def test_should_check_response_with_date(self) -> None:
        file_one = self.faker.word()
        file_two = self.faker.word()
        now_filter = self.faker.word()

        self.source_config_mock.get_source_file_filters.return_value = [f"{file_one}(date)", f"{file_two}(date)"]
        self.datetime_now_mock.strftime.return_value = now_filter

        with patch("pytz.timezone"):
            with patch("datetime.datetime") as date_time:
                date_time.now.return_value = self.datetime_now_mock
                response = self.mapper.get_files()

        self.assertListEqual(response, [f"{file_one}{now_filter}", f"{file_two}{now_filter}"])
