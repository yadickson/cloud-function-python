from unittest import TestCase

from faker import Faker
from parameterized import parameterized

from app.infrastructure.mapper.file_zip_info_mapper import FileZipInfoMapper


class TestFileZipInfoMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.mapper = FileZipInfoMapper()

    @parameterized.expand(
        [
            32,
            64,
            127,
            128,
            129,
            255,
            256,
            257,
            1023,
            1024,
            1025,
            20456,
        ]
    )
    def test_should_check_decompress_size(self, length: int) -> None:
        content = self.faker.zip(uncompressed_size=length, num_files=1, min_file_size=32, compression="deflate")
        response = self.mapper.get_decompress_size(content=content)
        self.assertEqual(response, length)

    @parameterized.expand(
        [
            32,
            64,
            127,
            128,
            129,
            255,
            256,
            257,
            1023,
            1024,
            1025,
            20456,
        ]
    )
    def test_should_check_file_name_size(self, length: int) -> None:
        content = self.faker.zip(uncompressed_size=length, num_files=1, min_file_size=32, compression="deflate")
        response = self.mapper.get_filename_size(content=content)
        self.assertEqual(response, 21)

    def test_should_check_file_name(self) -> None:
        content = self.faker.zip(uncompressed_size=256, num_files=1, min_file_size=32, compression="deflate")
        response = self.mapper.get_filename(content=content)
        self.assertIsNotNone(response)

    def test_should_check_body(self) -> None:
        content = self.faker.zip(uncompressed_size=256, num_files=1, min_file_size=32, compression="deflate")
        response = self.mapper.get_body(content=content)
        self.assertIsNotNone(response)
