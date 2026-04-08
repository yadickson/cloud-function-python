from injector import inject

from app.domain.model.file_model import FileModel
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.infrastructure.mapper.file_crypto_mapper_interface import FileCryptoMapperInterface
from app.infrastructure.security.pgp_gnupg_crypto_security_interface import PgpGnuPgCryptoSecurityInterface


class FileCryptoMapper(FileCryptoMapperInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        pgp_gnupg_crypto_security: PgpGnuPgCryptoSecurityInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.pgp_gnupg_crypto_security = pgp_gnupg_crypto_security

    def encode(self, file: FileModel) -> FileModel:
        try:
            filename = f"{file.filename}.PGP"
            content = self.pgp_gnupg_crypto_security.encode(content=file.content)
            return FileModel(filename=filename, content=content)
        except Exception as exception:
            self.logger_repository.error(message="Error to encode file.", cause=exception)
            return file
