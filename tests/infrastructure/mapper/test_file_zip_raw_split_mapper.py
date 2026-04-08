from unittest import TestCase

from faker import Faker

from app.infrastructure.mapper.file_zip_raw_split_mapper import FileZipRawSplitMapper


class TestFileZipRawSplitMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.mapper = FileZipRawSplitMapper()

    def test_should_check_empty_parts_when_input_is_empty(self) -> None:
        content = b""
        response = self.mapper.get_parts(content=content)
        self.assertListEqual(response, [])

    def test_should_check_empty_parts_when_file_is_not_zip_multi_files(self) -> None:
        content = b"\x51\x4b\x03\x04\x14\x01\x01\x01\x01\x01\x01\x51\x4b\x03\x04\x14\x02\x02\x02\x02"
        response = self.mapper.get_parts(content=content)
        self.assertListEqual(response, [])

    def test_should_check_one_part(self) -> None:
        content = b"\x50\x4b\x03\x04\x14\x01\x01\x01\x01\x01\x01"
        response = self.mapper.get_parts(content=content)
        self.assertListEqual(response, [b"\x50\x4b\x03\x04\x14\x01\x01\x01\x01\x01\x01"])

    def test_should_check_two_parts(self) -> None:
        content = b"\x50\x4b\x03\x04\x14\x01\x01\x01\x01\x01\x01\x50\x4b\x03\x04\x14\x02\x02\x02\x02"
        response = self.mapper.get_parts(content=content)
        self.assertListEqual(response, [b"\x50\x4b\x03\x04\x14\x01\x01\x01\x01\x01\x01", b"\x50\x4b\x03\x04\x14\x02\x02\x02\x02"])

    def test_should_check_faker_zip_deflate_parts(self) -> None:
        num_files = self.faker.random_int(min=10, max=20)
        content = self.faker.zip(uncompressed_size=64 * num_files, num_files=num_files, min_file_size=32, compression="deflate")

        response = self.mapper.get_parts(content=content)

        self.assertEqual(len(response), num_files)
        self.assertNotEqual(response[0], response[num_files - 1])
