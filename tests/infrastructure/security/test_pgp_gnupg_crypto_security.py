import shutil
from unittest import TestCase
from unittest.mock import MagicMock, patch

import gnupg
import pytest
from faker import Faker

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.certify_config_repository_interface import CertifyConfigRepositoryInterface
from app.infrastructure.exception.security_exception import SecurityException
from app.infrastructure.security.pgp_gnupg_crypto_security import PgpGnuPgCryptoSecurity


class TestPgpGnuPgCryptoSecurity(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.logger_repository_mock = MagicMock(LoggerRepositoryInterface)
        self.security_config_repository_mock = MagicMock(CertifyConfigRepositoryInterface)
        self.crypto = PgpGnuPgCryptoSecurity(
            logger_repository=self.logger_repository_mock,
            security_config_repository=self.security_config_repository_mock,
        )

    def test_should_check_gpg_encode_parameters(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        pubkey = self.faker.word()
        fingerprint = self.faker.word()
        data = self.faker.binary(length=128)

        gpg_mock = MagicMock(gnupg.GPG)
        import_keys_mock = gnupg.ImportResult(gpg_mock)
        result_mock = gnupg.Crypt(gpg_mock)

        import_keys_mock.count = 1
        import_keys_mock.fingerprints = [fingerprint]
        result_mock.data = data

        self.security_config_repository_mock.get_public_key.return_value = pubkey
        gpg_mock.import_keys.return_value = import_keys_mock
        gpg_mock.encrypt.return_value = result_mock

        with patch("gnupg.GPG") as gpg:
            gpg.return_value = gpg_mock
            response = self.crypto.encode(content=content)

        gpg.assert_called_once_with()
        gpg_mock.import_keys.assert_called_once_with(pubkey)
        gpg_mock.encrypt.assert_called_once_with(content, recipients=[fingerprint], always_trust=True)

        self.assertEqual(response, bytes(data))

    def test_should_check_gpg_encode_error(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        pubkey = self.faker.word()

        gpg_mock = MagicMock(gnupg.GPG)
        import_keys_mock = gnupg.ImportResult(gpg_mock)

        import_keys_mock.count = 0

        self.security_config_repository_mock.get_public_key.return_value = pubkey
        gpg_mock.import_keys.return_value = import_keys_mock

        with self.assertRaises(Exception) as context:
            with patch("gnupg.GPG") as gpg:
                gpg.return_value = gpg_mock
                self.crypto.encode(content=content)

        self.assertIsInstance(context.exception, SecurityException)
        self.assertEqual(context.exception.args[0], "Error to encode content.")
        self.assertIsInstance(context.exception.args[1], SecurityException)
        self.assertEqual(str(context.exception.args[1]), "Error to read public key.")

        call_args_list = self.logger_repository_mock.error.call_args_list

        self.assertEqual(call_args_list[0][1]["message"], "Error to encode content.")
        self.assertIsInstance(call_args_list[0][1]["cause"], SecurityException)

    def test_should_check_gpg_decode_parameters(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        key = self.faker.word()
        password = self.faker.word()
        data = self.faker.binary(length=128)

        gpg_mock = MagicMock(gnupg.GPG)
        import_keys_mock = gnupg.ImportResult(gpg_mock)
        result_mock = gnupg.Crypt(gpg_mock)

        import_keys_mock.count = 1
        result_mock.data = data

        self.security_config_repository_mock.get_private_key.return_value = key
        self.security_config_repository_mock.get_password.return_value = password

        gpg_mock.import_keys.return_value = import_keys_mock
        gpg_mock.decrypt.return_value = result_mock

        with patch("gnupg.GPG") as gpg:
            gpg.return_value = gpg_mock
            response = self.crypto.decode(content=content)

        gpg.assert_called_once_with()
        gpg_mock.import_keys.assert_called_once_with(key)
        gpg_mock.decrypt.assert_called_once_with(content, passphrase=password, always_trust=True)

        self.assertEqual(response, bytes(data))

    def test_should_check_gpg_decode_error(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        key = self.faker.word()
        password = self.faker.word()

        gpg_mock = MagicMock(gnupg.GPG)
        import_keys_mock = gnupg.ImportResult(gpg_mock)

        import_keys_mock.count = 0

        self.security_config_repository_mock.get_private_key.return_value = key
        self.security_config_repository_mock.get_password.return_value = password
        gpg_mock.import_keys.return_value = import_keys_mock

        with self.assertRaises(Exception) as context:
            with patch("gnupg.GPG") as gpg:
                gpg.return_value = gpg_mock
                self.crypto.decode(content=content)

        self.assertIsInstance(context.exception, SecurityException)
        self.assertEqual(context.exception.args[0], "Error to decode content.")
        self.assertIsInstance(context.exception.args[1], SecurityException)
        self.assertEqual(str(context.exception.args[1]), "Error to read private key.")

        call_args_list = self.logger_repository_mock.error.call_args_list

        self.assertEqual(call_args_list[0][1]["message"], "Error to decode content.")
        self.assertIsInstance(call_args_list[0][1]["cause"], SecurityException)

    @pytest.mark.skipif(shutil.which("gpg") is None, reason="GPG not found")
    def test_should_check_encode_and_decode_content(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        comment = self.faker.word()
        name = self.faker.name()
        email = self.faker.email()
        password = self.faker.password()
        params = {
            "Key-Type": "RSA",
            "Key-Length": 4096,
            "Name-Comment": comment,
            "Name-Real": name,
            "Name-Email": email,
            "Expire-Date": 365,
            "Passphrase": password,
        }

        gpg = gnupg.GPG()
        cmd = gpg.gen_key_input(**params)
        result = gpg.gen_key(cmd)

        pubkey = gpg.export_keys(result.fingerprint, secret=False, armor=True)
        key = gpg.export_keys(result.fingerprint, secret=True, armor=True, passphrase=password)

        self.security_config_repository_mock.get_public_key.return_value = str(pubkey)
        self.security_config_repository_mock.get_private_key.return_value = str(key)
        self.security_config_repository_mock.get_password.return_value = password

        encode_response = self.crypto.encode(content=content)

        self.assertIsNotNone(encode_response)
        self.assertNotEqual(encode_response, content)

        self.security_config_repository_mock.get_public_key.assert_called_once_with()

        decode_response = self.crypto.decode(content=encode_response)

        self.assertIsNotNone(decode_response)
        self.assertEqual(decode_response, content)

        self.security_config_repository_mock.get_private_key.assert_called_once_with()
        self.security_config_repository_mock.get_password.assert_called_once_with()

    @pytest.mark.skipif(shutil.which("gpg") is None, reason="GPG not found")
    def test_should_throws_security_exception_when_public_key_is_not_ok(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        password = self.faker.password()
        pubkey = self.faker.word()

        self.security_config_repository_mock.get_public_key.return_value = str(pubkey)
        self.security_config_repository_mock.get_password.return_value = password

        with self.assertRaises(Exception) as context:
            self.crypto.encode(content=content)

        self.assertIsInstance(context.exception, SecurityException)
        self.assertEqual(context.exception.args[0], "Error to encode content.")
        self.assertIsInstance(context.exception.args[1], SecurityException)
        self.assertEqual(str(context.exception.args[1]), "Error to read public key.")

    @pytest.mark.skipif(shutil.which("gpg") is None, reason="GPG not found")
    def test_should_throws_security_exception_when_private_key_is_not_ok(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")
        comment = self.faker.word()
        name = self.faker.name()
        email = self.faker.email()
        password = self.faker.password()
        key = self.faker.password()

        params = {
            "Key-Type": "RSA",
            "Key-Length": 4096,
            "Name-Comment": comment,
            "Name-Real": name,
            "Name-Email": email,
            "Expire-Date": 365,
            "Passphrase": password,
        }

        gpg = gnupg.GPG()
        cmd = gpg.gen_key_input(**params)
        result = gpg.gen_key(cmd)

        pubkey = gpg.export_keys(result.fingerprint, secret=False, armor=True)

        self.security_config_repository_mock.get_public_key.return_value = str(pubkey)
        self.security_config_repository_mock.get_private_key.return_value = str(key)
        self.security_config_repository_mock.get_password.return_value = password

        encode_response = self.crypto.encode(content=content)

        self.assertIsNotNone(encode_response)
        self.assertNotEqual(encode_response, content)

        self.security_config_repository_mock.get_public_key.assert_called_once_with()

        with self.assertRaises(Exception) as context:
            self.crypto.decode(content=encode_response)

        self.assertIsInstance(context.exception, SecurityException)
        self.assertEqual(context.exception.args[0], "Error to decode content.")
        self.assertIsInstance(context.exception.args[1], SecurityException)
        self.assertEqual(str(context.exception.args[1]), "Error to read private key.")

    @pytest.mark.skipif(shutil.which("gpg") is None, reason="GPG not found")
    def test_should_throws_security_exception_when_encode_fail(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")

        exception = Exception("error")

        self.security_config_repository_mock.get_public_key.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.crypto.encode(content=content)

        self.assertIsInstance(context.exception, SecurityException)
        self.logger_repository_mock.error.assert_called_once_with(message="Error to encode content.", cause=exception)
        self.assertEqual(context.exception.args[0], "Error to encode content.")
        self.assertEqual(context.exception.args[1], exception)

    @pytest.mark.skipif(shutil.which("gpg") is None, reason="GPG not found")
    def test_should_throws_security_exception_when_decode_fail(self) -> None:
        content = self.faker.zip(uncompressed_size=1024, num_files=10, min_file_size=32, compression="deflate")

        exception = Exception("error")

        self.security_config_repository_mock.get_private_key.side_effect = exception

        with self.assertRaises(Exception) as context:
            self.crypto.decode(content=content)

        self.assertIsInstance(context.exception, SecurityException)
        self.logger_repository_mock.error.assert_called_once_with(message="Error to decode content.", cause=exception)
        self.assertEqual(context.exception.args[0], "Error to decode content.")
        self.assertEqual(context.exception.args[1], exception)
