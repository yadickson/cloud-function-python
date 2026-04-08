import logging
from typing import Optional

import emoji
from injector import inject

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.logger.logger_extras_interface import LoggerExtrasInterface


class LoggerRepository(LoggerRepositoryInterface):
    @inject
    def __init__(self, logger: logging.Logger, extras: LoggerExtrasInterface) -> None:
        self.logger = logger
        self.extras = extras

    def running(self, message: str) -> None:
        self.logger.info(msg=f"{emoji.emojize(':fire:')} {message}", extra=self.extras.get_extras())

    def info(self, message: str) -> None:
        self.logger.info(msg=f"{emoji.emojize(':sparkles:')} {message}", extra=self.extras.get_extras())

    def warn(self, message: str, cause: Optional[Exception] = None) -> None:
        self.logger.warning(
            msg=f"{emoji.emojize(':red_exclamation_mark:')} {message} {('', str(cause))[cause is not None]}",
            exc_info=False,
            extra=self.extras.get_extras(),
        )

    def error(self, message: str, cause: Optional[Exception] = None) -> None:
        self.logger.error(
            msg=f"{emoji.emojize(':cross_mark:')} {message} {('', str(cause))[cause is not None]}", exc_info=False, extra=self.extras.get_extras()
        )

    def success(self, message: str) -> None:
        self.logger.info(msg=f"{emoji.emojize(':check_mark_button:')} {message}", extra=self.extras.get_extras())
