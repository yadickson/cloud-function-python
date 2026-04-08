import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch

from faker import Faker

from app.infrastructure.logger.logger_extras_interface import LoggerExtrasInterface
from app.infrastructure.logger.logger_repository import LoggerRepository


class TestLoggerRepository(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_mock = MagicMock(logging.Logger)
        self.extras_mock = MagicMock(LoggerExtrasInterface)

        self.repository = LoggerRepository(logger=self.logger_mock, extras=self.extras_mock)

    def test_should_check_logger_running_parameters(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.running(message=message)

        emoji_mock.assert_called_once_with(":fire:")
        self.logger_mock.info.assert_called_once_with(msg=f"{icon} {message}", extra=extras)

    def test_should_check_logger_info_parameters(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.info(message=message)

        emoji_mock.assert_called_once_with(":sparkles:")
        self.logger_mock.info.assert_called_once_with(msg=f"{icon} {message}", extra=extras)

    def test_should_check_logger_warn_parameters(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])
        exception = Exception("error")

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.warn(message=message, cause=exception)

        emoji_mock.assert_called_once_with(":red_exclamation_mark:")
        self.logger_mock.warning.assert_called_once_with(msg=f"{icon} {message} {str(exception)}", exc_info=False, extra=extras)

    def test_should_check_logger_warn_parameters_without_exception(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.warn(message=message)

        emoji_mock.assert_called_once_with(":red_exclamation_mark:")
        self.logger_mock.warning.assert_called_once_with(msg=f"{icon} {message} ", exc_info=False, extra=extras)

    def test_should_check_logger_error_parameters(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])
        exception = Exception("error")

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.error(message=message, cause=exception)

        emoji_mock.assert_called_once_with(":cross_mark:")
        self.logger_mock.error.assert_called_once_with(msg=f"{icon} {message} {str(exception)}", exc_info=False, extra=extras)

    def test_should_check_logger_error_parameters_without_exception(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.error(message=message)

        emoji_mock.assert_called_once_with(":cross_mark:")
        self.logger_mock.error.assert_called_once_with(msg=f"{icon} {message} ", exc_info=False, extra=extras)

    def test_should_check_logger_success_parameters(self) -> None:
        message = self.faker.word()
        icon = self.faker.word()
        extras = self.faker.pydict(nb_elements=2, value_types=[str])

        self.extras_mock.get_extras.return_value = extras

        with patch("emoji.emojize") as emoji_mock:
            emoji_mock.return_value = icon
            self.repository.success(message=message)

        emoji_mock.assert_called_once_with(":check_mark_button:")
        self.logger_mock.info.assert_called_once_with(msg=f"{icon} {message}", extra=extras)
