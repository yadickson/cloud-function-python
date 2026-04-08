from unittest import TestCase

from faker import Faker
from marshmallow import fields

from app.infrastructure.validator.required_integer_schema import required_integer_schema


class TestRequiredIntegerSchema(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()

    def test_should_check_type_response(self) -> None:
        field_name = self.faker.word()

        response = required_integer_schema(field_name=field_name)

        self.assertIsInstance(response, fields.Integer)

    def test_should_check_required_true(self) -> None:
        field_name = self.faker.word()

        response = required_integer_schema(field_name=field_name)

        self.assertTrue(response.required)

    def test_should_check_error_message_required(self) -> None:
        field_name = self.faker.word()

        response = required_integer_schema(field_name=field_name)

        self.assertIn("required", response.error_messages)
        self.assertEqual(response.error_messages["required"], f"{field_name} is required.")

    def test_should_check_error_message_null(self) -> None:
        field_name = self.faker.word()

        response = required_integer_schema(field_name=field_name)

        self.assertIn("null", response.error_messages)
        self.assertEqual(response.error_messages["null"], f"{field_name} is required.")

    def test_should_check_error_message_invalid(self) -> None:
        field_name = self.faker.word()

        response = required_integer_schema(field_name=field_name)

        self.assertIn("invalid", response.error_messages)
        self.assertEqual(response.error_messages["invalid"], f"{field_name} is required.")
