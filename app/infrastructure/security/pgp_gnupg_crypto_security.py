import gnupg
from injector import inject

from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.configuration.certify_config_repository_interface import CertifyConfigRepositoryInterface
from app.infrastructure.exception.security_exception import SecurityException
from app.infrastructure.security.pgp_gnupg_crypto_security_interface import PgpGnuPgCryptoSecurityInterface


class PgpGnuPgCryptoSecurity(PgpGnuPgCryptoSecurityInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        security_config_repository: CertifyConfigRepositoryInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.security_config_repository = security_config_repository

    def encode(self, content: bytes) -> bytes:
        try:
            gpg = gnupg.GPG()
            public_key = self.security_config_repository.get_public_key()
            import_result = gpg.import_keys(public_key)

            if import_result.count == 0:
                raise SecurityException("Error to read public key.")

            recipient_fingerprint = import_result.fingerprints[0]  # pragma: no mutate

            response = gpg.encrypt(content, recipients=[recipient_fingerprint], always_trust=True)

            return bytes(response.data)
        except Exception as exception:
            self.logger_repository.error(message="Error to encode content.", cause=exception)
            raise SecurityException("Error to encode content.", exception)

    def decode(self, content: bytes) -> bytes:
        try:
            gpg = gnupg.GPG()
            private_key = self.security_config_repository.get_private_key()
            password = self.security_config_repository.get_password()
            import_result = gpg.import_keys(private_key)

            if import_result.count == 0:
                raise SecurityException("Error to read private key.")

            response = gpg.decrypt(content, passphrase=password, always_trust=True)

            return bytes(response.data)
        except Exception as exception:
            self.logger_repository.error(message="Error to decode content.", cause=exception)
            raise SecurityException("Error to decode content.", exception)
