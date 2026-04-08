from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_crypto_mapper import FileCryptoMapper
from app.infrastructure.security.pgp_gnupg_crypto_security_interface import PgpGnuPgCryptoSecurityInterface


class TestFileCryptoMapper(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.pgp_gnupg_crypto_security_mock = MagicMock(PgpGnuPgCryptoSecurityInterface)

        self.mapper = FileCryptoMapper(
            logger_repository=self.logger_repository_mock,
            pgp_gnupg_crypto_security=self.pgp_gnupg_crypto_security_mock,
        )

    def test_should_check_response_reader_file_ok(self) -> None:
        filename = self.faker.file_name()
        content = self.faker.binary(length=64)
        encode = self.faker.binary(length=128)

        file = FileModel(filename=filename, content=content)

        self.pgp_gnupg_crypto_security_mock.encode.return_value = encode

        response = self.mapper.encode(file=file)

        self.assertIsInstance(response, FileModel)
        self.assertEqual(response.filename, f"{filename}.PGP")
        self.assertEqual(response.content, encode)

        self.pgp_gnupg_crypto_security_mock.encode.assert_called_once_with(content=content)

    def test_should_check_response_reader_file_is_nok(self) -> None:
        filename = self.faker.file_name()
        content = self.faker.binary(length=64)

        file = FileModel(filename=filename, content=content)

        exception = Exception("error")

        self.pgp_gnupg_crypto_security_mock.encode.side_effect = exception

        response = self.mapper.encode(file=file)

        self.logger_repository_mock.error.assert_called_once_with(message="Error to encode file.", cause=exception)

        self.assertIsInstance(response, FileModel)
        self.assertEqual(response.filename, filename)
        self.assertEqual(response.content, content)
