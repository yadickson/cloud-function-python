from pysftp import CnOpts

from app.infrastructure.connector.sftp_connector_options_interface import SftpConnectorOptionsInterface


class SftpConnectorOptions(SftpConnectorOptionsInterface):
    def get_options(self) -> CnOpts:
        options = CnOpts()
        options.hostkeys = None
        return options
