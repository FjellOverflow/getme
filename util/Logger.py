import enum
import sys
from typing import Optional

GETME_LOGGER_PREFIX = '[getme]: '


class GetMeLoggerMode(enum.Enum):
    VERBOSE = 0
    DEFAULT = 1
    QUIET = 2


class GetMeLogger:
    class __GetMeLogger:

        def __init__(self, mode: GetMeLoggerMode):
            self.__mode = mode

        def get_mode(self) -> GetMeLoggerMode:
            return self.__mode

    __singleton_instance = None

    def __init__(self, mode: Optional[GetMeLoggerMode]):
        if not GetMeLogger.__singleton_instance:
            GetMeLogger.__singleton_instance = GetMeLogger.__GetMeLogger(mode)

    @staticmethod
    def get_log_prefix() -> str:
        return GETME_LOGGER_PREFIX

    @staticmethod
    def get_mode() -> GetMeLoggerMode:
        return GetMeLogger.__singleton_instance.get_mode()

    @staticmethod
    def _log(message: str) -> None:
        print(f'{GETME_LOGGER_PREFIX}{message}')

    @staticmethod
    def log_verbose(message: str) -> None:
        if GetMeLogger.get_mode() is GetMeLoggerMode.VERBOSE:
            GetMeLogger._log(message)

    @staticmethod
    def log_default(message: str) -> None:
        if GetMeLogger.get_mode() is not GetMeLoggerMode.QUIET:
            GetMeLogger._log(message)

    @staticmethod
    def log_important(message: str) -> None:
        GetMeLogger._log(message)

    @staticmethod
    def log_and_exit(message: str) -> None:
        if GetMeLogger.get_mode() is not GetMeLoggerMode.QUIET:
            GetMeLogger._log(message)
            GetMeLogger._log('Exiting.')
        sys.exit()

    @staticmethod
    def log_and_abort(message: str) -> None:
        GetMeLogger._log(message)
        GetMeLogger._log('Aborting.')
        sys.exit(1)
