from injector import inject

from app.domain.repository.del_files_repository_interface import DelFilesRepositoryInterface
from app.domain.repository.get_files_repository_interface import GetFilesRepositoryInterface
from app.domain.repository.logger_repository_interface import LoggerRepositoryInterface
from app.domain.repository.send_files_repository_interface import SendFilesRepositoryInterface
from app.domain.use_case.transfer_files_use_case_interface import TransferFilesUseCaseInterface


class TransferFilesUseCase(TransferFilesUseCaseInterface):
    @inject
    def __init__(
        self,
        logger_repository: LoggerRepositoryInterface,
        get_files_repository: GetFilesRepositoryInterface,
        send_files_repository: SendFilesRepositoryInterface,
        del_files_repository: DelFilesRepositoryInterface,
    ) -> None:
        self.logger_repository = logger_repository
        self.get_files_repository = get_files_repository
        self.send_files_repository = send_files_repository
        self.del_files_repository = del_files_repository

    def execute(self) -> None:
        self.logger_repository.running(message="Starting files transfer.")
        files = self.get_files_repository.execute()
        self.send_files_repository.execute(files=files)
        self.del_files_repository.execute()
        self.logger_repository.success(message=f"Files transferred [{len(files)}]." if files else "There are no files to transmit.")
