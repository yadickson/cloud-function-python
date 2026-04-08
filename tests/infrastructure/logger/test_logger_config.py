import logging
import time
from unittest import TestCase
from unittest.mock import MagicMock, patch

from faker import Faker

from app.infrastructure.logger.logger_config import logger_config


class TestLoggerConfig(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_mock = MagicMock(logging.Logger)
        self.logger_console_mock = MagicMock(logging.Handler)
        self.logger_formatter_mock = MagicMock(logging.Formatter)

    def test_should_check_app_logger_name(self) -> None:
        with patch("logging.getLogger") as mock_instance:
            logger_config()

        mock_instance.assert_called_once_with("application")

    def test_should_check_logger_created(self) -> None:
        with patch("logging.getLogger") as mock_instance:
            mock_instance.return_value = self.logger_mock

            response = logger_config()

            self.assertEqual(response, self.logger_mock)

    def test_should_check_app_logger_level(self) -> None:
        with patch("logging.getLogger") as mock_instance:
            mock_instance.return_value = self.logger_mock

            logger_config()

        self.logger_mock.setLevel.assert_called_once_with(logging.INFO)

    def test_should_check_app_logger_console(self) -> None:
        with patch("logging.StreamHandler") as mock_instance:
            logger_config()

        mock_instance.assert_called_once_with()

    def test_should_check_app_logger_console_level(self) -> None:
        with patch("logging.StreamHandler") as mock_instance:
            mock_instance.return_value = self.logger_console_mock

            logger_config()

        self.logger_console_mock.setLevel.assert_called_once_with(logging.INFO)

    def test_should_check_app_logger_formatter_converter(self) -> None:
        logger_config()
        self.assertEqual(time.localtime, logging.Formatter.converter)

    def test_should_check_app_logger_console_formatter(self) -> None:
        with patch("logging.Formatter") as mock_instance:
            logger_config()

        mock_instance.assert_called_once_with(fmt="[%(levelname)5s] [%(logger_info)s] - %(message)s")

    def test_should_check_app_logger_console_formatter_logging(self) -> None:
        formatter = MagicMock(logging.Formatter)

        with patch("logging.StreamHandler") as mock_instance:
            mock_instance.return_value = self.logger_console_mock
            with patch("logging.Formatter") as mock_formatter_instance:
                mock_formatter_instance.return_value = formatter
                logger_config()

        self.logger_console_mock.setFormatter.assert_called_once_with(formatter)

    def test_should_check_app_logger_console_handler(self) -> None:
        with patch("logging.getLogger") as mock_instance:
            mock_instance.return_value = self.logger_mock

            with patch("logging.StreamHandler") as mock_console_instance:
                mock_console_instance.return_value = self.logger_console_mock
                logger_config()

        self.logger_mock.addHandler.assert_called_once_with(self.logger_console_mock)
