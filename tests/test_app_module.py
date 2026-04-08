import logging
from typing import Any
from unittest import TestCase
from unittest.mock import MagicMock

from faker import Faker
from injector import Binder, singleton

from app.app_module import AppModule
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


class TestAppModule(TestCase):
    def setUp(self) -> None:
        self.faker = Faker()
        self.module = AppModule()
        self.binder_mock = MagicMock(Binder)

    def find_logger(self) -> Any:
        elements = [
            arg
            for arg in self.binder_mock.bind.call_args_list
            if arg[1]["interface"] == logging.Logger and isinstance(arg[1]["to"], logging.Logger) and arg[1]["scope"] == singleton
        ]
        return next(iter(elements or []), None)

    def find_full(self, interface: Any, clazz: Any) -> Any:
        elements = [arg for arg in self.binder_mock.bind.call_args_list if arg[1]["interface"] == interface and arg[1]["to"] == clazz]
        return next(iter(elements or []), None)

    def test_should_check_binder_count(self) -> None:
        self.module.configure(self.binder_mock)
        call_count = self.binder_mock.bind.call_count
        self.assertEqual(call_count, 47)

    def test_should_check_logger_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_logger())

    def test_should_check_logger_extras_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(LoggerExtrasInterface, LoggerExtras))

    def test_should_check_load_config_use_case_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(LoadConfigUseCaseInterface, LoadConfigUseCase))

    def test_should_check_transfer_file_use_case_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(TransferFilesUseCaseInterface, TransferFilesUseCase))

    def test_should_check_config_validator_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(ConfigValidatorInterface, ConfigValidator))

    def test_should_check_timezone_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(TimeZoneConfigRepositoryInterface, TimeZoneConfigRepository))

    def test_should_check_source_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SourceConfigRepositoryInterface, SourceConfigRepository))

    def test_should_check_destination_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(DestinationConfigRepositoryInterface, DestinationConfigRepository))

    def test_should_check_logger_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(LoggerRepositoryInterface, LoggerRepository))

    def test_should_check_del_files_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(DelFilesRepositoryInterface, DelFilesRepository))

    def test_should_check_get_files_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(GetFilesRepositoryInterface, GetFilesRepository))

    def test_should_check_send_files_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SendFilesRepositoryInterface, SendFilesRepository))

    def test_should_check_del_file_gateway_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(DelFileGatewayInterface, DelFileGateway))

    def test_should_check_get_file_gateway_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(GetFileGatewayInterface, GetFileGateway))

    def test_should_check_get_files_gateway_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(GetFilesGatewayInterface, GetFilesGateway))

    def test_should_check_send_file_gateway_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SendFileGatewayInterface, SendFileGateway))

    def test_should_check_sftp_connector_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SftpConnectorInterface, SftpConnector))

    def test_should_check_sftp_connector_options_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SftpConnectorOptionsInterface, SftpConnectorOptions))

    def test_should_check_files_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesMapperInterface, FilesMapper))

    def test_should_check_file_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileMapperInterface, FileMapper))

    def test_should_check_file_compress_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileCompressMapperInterface, FileCompressMapper))

    def test_should_check_file_decompress_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileDecompressMapperInterface, FileDecompressMapper))

    def test_should_check_file_zip_raw_reader_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileZipRawReaderMapperInterface, FileZipRawReaderMapper))

    def test_should_check_file_zip_raw_split_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileZipRawSplitMapperInterface, FileZipRawSplitMapper))

    def test_should_check_file_zip_reader_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileZipReaderMapperInterface, FileZipReaderMapper))

    def test_should_check_file_csv_split_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileCsvSplitMapperInterface, FileCsvSplitMapper))

    def test_should_check_files_csv_split_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesCsvSplitMapperInterface, FilesCsvSplitMapper))

    def test_should_check_file_group_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesGroupMapperInterface, FilesGroupMapper))

    def test_should_check_file_csv_group_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileCsvGroupMapperInterface, FileCsvGroupMapper))

    def test_should_check_files_search_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesSearchMapperInterface, FilesSearchMapper))

    def test_should_check_files_compress_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesCompressMapperInterface, FilesCompressMapper))

    def test_should_check_files_filtered_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesFilteredMapperInterface, FilesFilteredMapper))

    def test_should_check_files_filters_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FilesFiltersMapperInterface, FilesFiltersMapper))

    def test_should_check_file_csv_key_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileCsvKeyMapperInterface, FileCsvKeyMapper))

    def test_should_check_file_decompress_raw_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileDecompressRawMapperInterface, FileDecompressRawMapper))

    def test_should_check_file_decompress_full_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileDecompressFullMapperInterface, FileDecompressFullMapper))

    def test_should_check_file_zip_info_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileZipInfoMapperInterface, FileZipInfoMapper))

    def test_should_check_file_crypto_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(FileCryptoMapperInterface, FileCryptoMapper))

    def test_should_check_pgp_gnupg_crypto_security_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(PgpGnuPgCryptoSecurityInterface, PgpGnuPgCryptoSecurity))

    def test_should_check_certify_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(CertifyConfigRepositoryInterface, CertifyConfigRepository))

    def test_should_check_secret_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SecretConfigRepositoryInterface, SecretConfigRepository))

    def test_should_check_base64_security_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(Base64SecurityInterface, Base64Security))

    def test_should_check_secret_manager_security_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(SecretManagerSecurityInterface, SecretManagerSecurity))

    def test_should_check_environment_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(EnvironmentConfigRepositoryInterface, EnvironmentConfigRepository))

    def test_should_check_config_repository_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(ConfigRepositoryInterface, ConfigRepository))

    def test_should_check_config_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(ConfigMapperInterface, ConfigMapper))

    def test_should_check_config_merge_mapper_binder(self) -> None:
        self.module.configure(self.binder_mock)
        self.assertIsNotNone(self.find_full(ConfigMergeMapperInterface, ConfigMergeMapper))
