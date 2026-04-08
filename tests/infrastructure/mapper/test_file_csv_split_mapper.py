from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.domain.model.file_model import FileModel
from app.infrastructure.mapper.file_csv_group_mapper_interface import FileCsvGroupMapperInterface
from app.infrastructure.mapper.file_csv_key_mapper_interface import FileCsvKeyMapperInterface
from app.infrastructure.mapper.file_csv_split_mapper import FileCsvSplitMapper


class TestFileCsvSplitMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.csv_group_mapper_mock = MagicMock(FileCsvGroupMapperInterface)
        self.csv_key_mapper_mock = MagicMock(FileCsvKeyMapperInterface)

        self.mapper = FileCsvSplitMapper(
            csv_group_mapper=self.csv_group_mapper_mock,
            csv_key_mapper=self.csv_key_mapper_mock,
        )

    def test_should_check_group_parameters(self) -> None:
        filename = self.faker.word()
        content = b""

        self.csv_group_mapper_mock.group.return_value = []

        file = FileModel(filename=filename, content=content)

        self.mapper.split(file=file)

        self.csv_group_mapper_mock.group.assert_called_once_with(file=file)

    def test_should_check_empty_response_when_group_is_empty(self) -> None:
        filename = self.faker.word()
        content = b""

        self.csv_group_mapper_mock.group.return_value = []

        file = FileModel(filename=filename, content=content)

        response = self.mapper.split(file=file)

        self.assertListEqual(response, [])

    def test_should_check_response_when_group_has_one_element(self) -> None:
        filename = self.faker.word()
        extension = self.faker.word()
        content = b""

        line_one = self.faker.binary(length=64)
        key_one = self.faker.word()

        self.csv_group_mapper_mock.group.return_value = [[line_one]]
        self.csv_key_mapper_mock.get_key.return_value = key_one

        file = FileModel(filename=f"{filename}.{extension}", content=content)

        response = self.mapper.split(file=file)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].filename, f"{filename}_1.{extension}")
        self.assertEqual(response[0].content, line_one)
        self.assertListEqual(response[0].relations, [key_one])

        self.csv_key_mapper_mock.get_key.assert_called_once_with(line=line_one)

    def test_should_check_response_when_group_has_two_elements(self) -> None:
        filename = self.faker.word()
        extension = self.faker.word()
        content = b""

        line_one = self.faker.binary(length=64)
        line_two = self.faker.binary(length=64)
        key_one = self.faker.word()
        key_two = self.faker.word()

        self.csv_group_mapper_mock.group.return_value = [[line_one, line_two]]
        self.csv_key_mapper_mock.get_key.side_effect = [key_one, key_two]

        file = FileModel(filename=f"{filename}.{extension}", content=content)

        response = self.mapper.split(file=file)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].filename, f"{filename}_1.{extension}")
        self.assertEqual(response[0].content, b"\n".join([line_one, line_two]))
        self.assertListEqual(response[0].relations, [key_one, key_two])

    def test_should_check_response_when_has_two_groups(self) -> None:
        filename = self.faker.word()
        extension = self.faker.word()
        content = b""

        line_one = self.faker.binary(length=64)
        line_two = self.faker.binary(length=64)
        key_one = self.faker.word()
        key_two = self.faker.word()

        self.csv_group_mapper_mock.group.return_value = [[line_one], [line_two]]
        self.csv_key_mapper_mock.get_key.side_effect = [key_one, key_two]

        file = FileModel(filename=f"{filename}.{extension}", content=content)

        response = self.mapper.split(file=file)

        self.assertEqual(len(response), 2)

        self.assertEqual(response[0].filename, f"{filename}_1.{extension}")
        self.assertEqual(response[0].content, line_one)
        self.assertListEqual(response[0].relations, [key_one])

        self.assertEqual(response[1].filename, f"{filename}_2.{extension}")
        self.assertEqual(response[1].content, line_two)
        self.assertListEqual(response[1].relations, [key_two])
