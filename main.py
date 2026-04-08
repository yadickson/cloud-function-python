import flask
import functions_framework
from dotenv import load_dotenv
from google.cloud import logging
from injector import Injector

from app.app_module import AppModule
from app.domain.use_case.load_config_use_case_interface import LoadConfigUseCaseInterface
from app.domain.use_case.transfer_files_use_case_interface import TransferFilesUseCaseInterface

load_dotenv()
logging.Client().setup_logging()
injector = Injector([AppModule()])

load_config_use_case = injector.get(LoadConfigUseCaseInterface)
transfer_file_use_case = injector.get(TransferFilesUseCaseInterface)

load_config_use_case.execute()


@functions_framework.errorhandler(Exception)
def handle_error(error: Exception) -> flask.typing.ResponseReturnValue:
    return {"message": "There is and error, please contact to admin."}, 500


@functions_framework.http
def execute(request: flask.Request) -> flask.typing.ResponseReturnValue:
    transfer_file_use_case.execute()
    return {"message": "Transfer completed successfully."}, 200
