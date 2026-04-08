from unittest import TestCase

from app.infrastructure.mapper.file_csv_key_mapper import FileCsvKeyMapper


class TestFileCsvKeyMapper(TestCase):
    def setUp(self) -> None:
        self.mapper = FileCsvKeyMapper()

    def test_should_check_key_without_dots_or_dash(self) -> None:
        line = b"abcd;123456"
        response = self.mapper.get_key(line=line)
        self.assertEqual(response, "123456")

    def test_should_check_key_with_dots_and_dash(self) -> None:
        line = b"abcd;1.234.567-8"
        response = self.mapper.get_key(line=line)
        self.assertEqual(response, "1234567")
