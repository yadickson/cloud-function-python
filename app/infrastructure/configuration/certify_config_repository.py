from injector import inject

from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.infrastructure.configuration.certify_config_repository_interface import CertifyConfigRepositoryInterface
from app.infrastructure.security.base64_security_interface import Base64SecurityInterface


class CertifyConfigRepository(CertifyConfigRepositoryInterface):
    @inject
    def __init__(
        self,
        config_repository: ConfigRepositoryInterface,
        base64_security: Base64SecurityInterface,
    ) -> None:
        self.config_repository = config_repository
        self.base64_security = base64_security

    def get_public_key(self) -> str:
        content = self.config_repository.get_configuration().pgp_public_key
        return self.base64_security.decode(content=content)

    def get_private_key(self) -> str:
        content = self.config_repository.get_configuration().pgp_private_key
        return self.base64_security.decode(content=content)

    def get_password(self) -> str:
        return self.config_repository.get_configuration().pgp_password
