from structlog import BoundLogger, get_logger


class LogMixin:
    def __init__(self):
        self._logger = get_logger()

    @property
    def log(self) -> BoundLogger:
        return self._logger
