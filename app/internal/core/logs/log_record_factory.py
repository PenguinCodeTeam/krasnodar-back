from logging import LogRecord
from typing import Callable

from internal.core.requests import request_id_var


class LogRecordFactory:
    """Фабрика для добавления важной контекстуальной информации для логирования.
    Добавляет в записи id запроса
    """

    def __init__(self, original_factory: Callable):
        """Конструктор класса

        Args:
            original_factory: Изначальная фабрика, которая получается путём вызрова logging.getLogRecordFactory()
        """
        self.original_factory = original_factory

    def __call__(self, *args, **kwargs) -> LogRecord:
        record = self.original_factory(*args, **kwargs)
        record.req_id = request_id_var.get()
        return record
