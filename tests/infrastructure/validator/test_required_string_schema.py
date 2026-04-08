from unittest import TestCase

from faker import Faker
from marshmallow import fields, validate

from app.infrastructure.validator.required_string_schema import required_string_schema


class TestRequiredStringSchema(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()

    def test_should_check_type_response(self) -> None:
        field_name = self.faker.word()

        response = required_string_schema(field_name=field_name)

        self.assertIsInstance(response, fields.String)

    def test_should_check_required_true(self) -> None:
        field_name = self.faker.word()

        response = required_string_schema(field_name=field_name)

        self.assertTrue(response.required)

    def test_should_check_validate(self) -> None:
        field_name = self.faker.word()

        response = required_string_schema(field_name=field_name)

        self.assertIsInstance(response.validate, validate.Length)
        self.assertEqual(response.validate.min, 1)
        self.assertEqual(response.validate.error, f"{field_name} is required.")

    def test_should_check_error_message_required(self) -> None:
        field_name = self.faker.word()

        response = required_string_schema(field_name=field_name)

        self.assertIn("required", response.error_messages)
        self.assertEqual(response.error_messages["required"], f"{field_name} is required.")

    def test_should_check_error_message_null(self) -> None:
        field_name = self.faker.word()

        response = required_string_schema(field_name=field_name)

        self.assertIn("null", response.error_messages)
        self.assertEqual(response.error_messages["null"], f"{field_name} is required.")
