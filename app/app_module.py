import logging

from injector import Binder, Module, singleton

from app.domain.repository.config_repository_interface import ConfigRepositoryInterface
from app.domain.repository.del_files_repository_interface import DelFilesRepositoryInterface
from app.domain.repository.get_files_repository_interface import GetFilesRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.repository.send_files_repository_interface import SendFilesRepositoryInterface
from app.domain.use_case.load_config_use_case import LoadConfigUseCase
from app.domain.use_case.load_config_use_case_interface import LoadConfigUseCaseInterface
from app.domain.use_case.transfer_files_use_case import TransferFilesUseCase
from app.domain.use_case.transfer_files_use_case_interface import TransferFilesUseCaseInterface
from app.domain.validator.config_validator_interface import ConfigValidatorInterface
from app.infrastructure.configuration.certify_config_repository import CertifyConfigRepository
from app.infrastructure.configuration.certify_config_repository_interface import CertifyConfigRepositoryInterface
from app.infrastructure.configuration.destination_config_repository import DestinationConfigRepository
from app.infrastructure.configuration.destination_config_repository_interface import DestinationConfigRepositoryInterface
from app.infrastructure.configuration.environment_config_repository import EnvironmentConfigRepository
from app.infrastructure.configuration.environment_config_repository_interface import EnvironmentConfigRepositoryInterface
from app.infrastructure.configuration.secret_config_repository import SecretConfigRepository
from app.infrastructure.configuration.secret_config_repository_interface import SecretConfigRepositoryInterface
from app.infrastructure.configuration.source_config_repository import SourceConfigRepository
from app.infrastructure.configuration.source_config_repository_interface import SourceConfigRepositoryInterface
from app.infrastructure.configuration.timezone_config_repository import TimeZoneConfigRepository
from app.infrastructure.configuration.timezone_config_repository_interface import TimeZoneConfigRepositoryInterface
from app.infrastructure.connector.sftp_connector import SftpConnector
from app.infrastructure.connector.sftp_connector_interface import SftpConnectorInterface
from app.infrastructure.connector.sftp_connector_options import SftpConnectorOptions
from app.infrastructure.connector.sftp_connector_options_interface import SftpConnectorOptionsInterface
from app.infrastructure.gateway.del_file_gateway import DelFileGateway
from app.infrastructure.gateway.del_file_gateway_interface import DelFileGatewayInterface
from app.infrastructure.gateway.get_file_gateway import GetFileGateway
from app.infrastructure.gateway.get_file_gateway_interface import GetFileGatewayInterface
from app.infrastructure.gateway.get_files_gateway import GetFilesGateway
from app.infrastructure.gateway.get_files_gateway_interface import GetFilesGatewayInterface
from app.infrastructure.gateway.send_file_gateway import SendFileGateway
from app.infrastructure.gateway.send_file_gateway_interface import SendFileGatewayInterface
from app.infrastructure.logger.logger_config import logger_config
from app.infrastructure.logger.logger_extras import LoggerExtras
from app.infrastructure.logger.logger_extras_interface import LoggerExtrasInterface
from app.infrastructure.logger.logger_repository import LoggerRepository
from app.infrastructure.mapper.config_mapper import ConfigMapper
from app.infrastructure.mapper.config_mapper_interface import ConfigMapperInterface
from app.infrastructure.mapper.config_merge_mapper import ConfigMergeMapper
from app.infrastructure.mapper.config_merge_mapper_interface import ConfigMergeMapperInterface
from app.infrastructure.mapper.file_compress_mapper import FileCompressMapper
from app.infrastructure.mapper.file_compress_mapper_interface import FileCompressMapperInterface
from app.infrastructure.mapper.file_crypto_mapper import FileCryptoMapper
from app.infrastructure.mapper.file_crypto_mapper_interface import FileCryptoMapperInterface
from app.infrastructure.mapper.file_csv_group_mapper import FileCsvGroupMapper
from app.infrastructure.mapper.file_csv_group_mapper_interface import FileCsvGroupMapperInterface
from app.infrastructure.mapper.file_csv_key_mapper import FileCsvKeyMapper
from app.infrastructure.mapper.file_csv_key_mapper_interface import FileCsvKeyMapperInterface
from app.infrastructure.mapper.file_csv_split_mapper import FileCsvSplitMapper
from app.infrastructure.mapper.file_csv_split_mapper_interface import FileCsvSplitMapperInterface
from app.infrastructure.mapper.file_decompress_full_mapper import FileDecompressFullMapper
from app.infrastructure.mapper.file_decompress_full_mapper_interface import FileDecompressFullMapperInterface
from app.infrastructure.mapper.file_decompress_mapper import FileDecompressMapper
from app.infrastructure.mapper.file_decompress_mapper_interface import FileDecompressMapperInterface
from app.infrastructure.mapper.file_decompress_raw_mapper import FileDecompressRawMapper
from app.infrastructure.mapper.file_decompress_raw_mapper_interface import FileDecompressRawMapperInterface
from app.infrastructure.mapper.file_mapper import FileMapper
from app.infrastructure.mapper.file_mapper_interface import FileMapperInterface
from app.infrastructure.mapper.file_zip_info_mapper import FileZipInfoMapper
from app.infrastructure.mapper.file_zip_info_mapper_interface import FileZipInfoMapperInterface
from app.infrastructure.mapper.file_zip_raw_reader_mapper import FileZipRawReaderMapper
from app.infrastructure.mapper.file_zip_raw_reader_mapper_interface import FileZipRawReaderMapperInterface
from app.infrastructure.mapper.file_zip_raw_split_mapper import FileZipRawSplitMapper
from app.infrastructure.mapper.file_zip_raw_split_mapper_interface import FileZipRawSplitMapperInterface
from app.infrastructure.mapper.file_zip_reader_mapper import FileZipReaderMapper
from app.infrastructure.mapper.file_zip_reader_mapper_interface import FileZipReaderMapperInterface
from app.infrastructure.mapper.files_compress_mapper import FilesCompressMapper
from app.infrastructure.mapper.files_compress_mapper_interface import FilesCompressMapperInterface
from app.infrastructure.mapper.files_csv_split_mapper import FilesCsvSplitMapper
from app.infrastructure.mapper.files_csv_split_mapper_interface import FilesCsvSplitMapperInterface
from app.infrastructure.mapper.files_filtered_mapper import FilesFilteredMapper
from app.infrastructure.mapper.files_filtered_mapper_interface import FilesFilteredMapperInterface
from app.infrastructure.mapper.files_filters_mapper import FilesFiltersMapper
from app.infrastructure.mapper.files_filters_mapper_interface import FilesFiltersMapperInterface
from app.infrastructure.mapper.files_group_mapper import FilesGroupMapper
from app.infrastructure.mapper.files_group_mapper_interface import FilesGroupMapperInterface
from app.infrastructure.mapper.files_mapper import FilesMapper
from app.infrastructure.mapper.files_mapper_interface import FilesMapperInterface
from app.infrastructure.mapper.files_search_mapper import FilesSearchMapper
from app.infrastructure.mapper.files_search_mapper_interface import FilesSearchMapperInterface
from app.infrastructure.repository.config_repository import ConfigRepository
from app.infrastructure.repository.del_files_repository import DelFilesRepository
from app.infrastructure.repository.get_files_repository import GetFilesRepository
from app.infrastructure.repository.send_files_repository import SendFilesRepository
from app.infrastructure.security.base64_security import Base64Security
from app.infrastructure.security.base64_security_interface import Base64SecurityInterface
from app.infrastructure.security.pgp_gnupg_crypto_security import PgpGnuPgCryptoSecurity
from app.infrastructure.security.pgp_gnupg_crypto_security_interface import PgpGnuPgCryptoSecurityInterface
from app.infrastructure.security.secret_manager_security import SecretManagerSecurity
from app.infrastructure.security.secret_manager_security_interface import SecretManagerSecurityInterface
from app.infrastructure.validator.config_validator import ConfigValidator


class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interface=logging.Logger, to=logger_config(), scope=singleton)
        binder.bind(interface=LoggerExtrasInterface, to=LoggerExtras)
        binder.bind(interface=LoadConfigUseCaseInterface, to=LoadConfigUseCase)
        binder.bind(interface=TransferFilesUseCaseInterface, to=TransferFilesUseCase)
        binder.bind(interface=ConfigValidatorInterface, to=ConfigValidator)
        binder.bind(interface=TimeZoneConfigRepositoryInterface, to=TimeZoneConfigRepository)
        binder.bind(interface=CertifyConfigRepositoryInterface, to=CertifyConfigRepository)
        binder.bind(interface=SourceConfigRepositoryInterface, to=SourceConfigRepository)
        binder.bind(interface=DestinationConfigRepositoryInterface, to=DestinationConfigRepository)
        binder.bind(interface=LoggerRepositoryInterface, to=LoggerRepository)
        binder.bind(interface=DelFilesRepositoryInterface, to=DelFilesRepository)
        binder.bind(interface=GetFilesRepositoryInterface, to=GetFilesRepository)
        binder.bind(interface=SendFilesRepositoryInterface, to=SendFilesRepository)
        binder.bind(interface=GetFilesGatewayInterface, to=GetFilesGateway)
        binder.bind(interface=GetFileGatewayInterface, to=GetFileGateway)
        binder.bind(interface=DelFileGatewayInterface, to=DelFileGateway)
        binder.bind(interface=SendFileGatewayInterface, to=SendFileGateway)
        binder.bind(interface=SftpConnectorInterface, to=SftpConnector)
        binder.bind(interface=SftpConnectorOptionsInterface, to=SftpConnectorOptions)
        binder.bind(interface=FilesMapperInterface, to=FilesMapper)
        binder.bind(interface=FileMapperInterface, to=FileMapper)
        binder.bind(interface=FileZipReaderMapperInterface, to=FileZipReaderMapper)
        binder.bind(interface=FileZipRawReaderMapperInterface, to=FileZipRawReaderMapper)
        binder.bind(interface=FileZipRawSplitMapperInterface, to=FileZipRawSplitMapper)
        binder.bind(interface=FileDecompressMapperInterface, to=FileDecompressMapper)
        binder.bind(interface=FilesGroupMapperInterface, to=FilesGroupMapper)
        binder.bind(interface=FileCompressMapperInterface, to=FileCompressMapper)
        binder.bind(interface=FileCsvSplitMapperInterface, to=FileCsvSplitMapper)
        binder.bind(interface=FilesCsvSplitMapperInterface, to=FilesCsvSplitMapper)
        binder.bind(interface=FileCsvGroupMapperInterface, to=FileCsvGroupMapper)
        binder.bind(interface=FilesSearchMapperInterface, to=FilesSearchMapper)
        binder.bind(interface=FilesCompressMapperInterface, to=FilesCompressMapper)
        binder.bind(interface=FileZipInfoMapperInterface, to=FileZipInfoMapper)
        binder.bind(interface=FileDecompressFullMapperInterface, to=FileDecompressFullMapper)
        binder.bind(interface=FileDecompressRawMapperInterface, to=FileDecompressRawMapper)
        binder.bind(interface=FileCsvKeyMapperInterface, to=FileCsvKeyMapper)
        binder.bind(interface=FilesFiltersMapperInterface, to=FilesFiltersMapper)
        binder.bind(interface=FilesFilteredMapperInterface, to=FilesFilteredMapper)
        binder.bind(interface=FileCryptoMapperInterface, to=FileCryptoMapper)
        binder.bind(interface=PgpGnuPgCryptoSecurityInterface, to=PgpGnuPgCryptoSecurity)
        binder.bind(interface=Base64SecurityInterface, to=Base64Security)
        binder.bind(interface=SecretConfigRepositoryInterface, to=SecretConfigRepository)
        binder.bind(interface=SecretManagerSecurityInterface, to=SecretManagerSecurity)
        binder.bind(interface=EnvironmentConfigRepositoryInterface, to=EnvironmentConfigRepository)
        binder.bind(interface=ConfigRepositoryInterface, to=ConfigRepository)
        binder.bind(interface=ConfigMapperInterface, to=ConfigMapper)
        binder.bind(interface=ConfigMergeMapperInterface, to=ConfigMergeMapper)
