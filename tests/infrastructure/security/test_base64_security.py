from unittest import TestCase

from faker import Faker

from app.infrastructure.security.base64_security import Base64Security


class TestBase64Security(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.security = Base64Security()

    def test_should_check_encode_and_decode_text(self) -> None:
        value = self.faker.word()

        response = self.security.encode(value)

        self.assertNotEqual(response, value)

        response = self.security.decode(response)

        self.assertEqual(response, value)
