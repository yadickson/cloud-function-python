from unittest import TestCase

from pysftp import CnOpts

from app.infrastructure.connector.sftp_connector_options import SftpConnectorOptions


class TestSftpConnectorOptions(TestCase):
    def setUp(self) -> None:
        self.connector_options = SftpConnectorOptions()

    def test_should_check_instance_and_flag_host_keys_disabled(self) -> None:
        options = self.connector_options.get_options()

        self.assertIsInstance(options, CnOpts)
        self.assertEqual(options.hostkeys, None)
