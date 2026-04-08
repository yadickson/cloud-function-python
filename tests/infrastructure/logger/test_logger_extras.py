import re
from unittest import TestCase

from app.infrastructure.logger.logger_extras import LoggerExtras


class TestLoggerExtras(TestCase):
    def setUp(self) -> None:
        self.logger_extras = LoggerExtras()

    def test_should_check_response_logger_info(self) -> None:
        response = self.logger_extras.get_extras()

        regex = re.compile(r".+:.+:\d+$")

        self.assertIsNotNone(response)
        self.assertListEqual(["logger_info"], list(response.keys()))
        self.assertTrue(regex.search(response["logger_info"]))
