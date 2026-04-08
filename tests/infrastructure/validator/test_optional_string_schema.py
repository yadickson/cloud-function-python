from unittest import TestCase

from faker import Faker
from marshmallow import fields

from app.infrastructure.validator.optional_string_schema import optional_string_schema


class TestOptionalStringSchema(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()

    def test_should_check_type_response(self) -> None:
        field_name = self.faker.word()

        response = optional_string_schema(field_name=field_name)

        self.assertIsInstance(response, fields.String)

    def test_should_check_allow_none_true(self) -> None:
        field_name = self.faker.word()

        response = optional_string_schema(field_name=field_name)

        self.assertTrue(response.allow_none)

    def test_should_check_error_message_invalid(self) -> None:
        field_name = self.faker.word()

        response = optional_string_schema(field_name=field_name)

        self.assertIn("invalid", response.error_messages)
        self.assertEqual(response.error_messages["invalid"], f"{field_name} is not ok.")
