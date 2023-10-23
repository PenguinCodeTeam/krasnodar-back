import json
from logging import Logger, LoggerAdapter
from typing import Any, MutableMapping, Optional


REQUESTS_MSG_FORMAT = '%(type)s: %(params)s %(msg)s'
ERROR_MSG_FORMAT = '%(traceback)s'


class BaseAdapter(LoggerAdapter):
    def __init__(self, logger: Logger, extra: Optional[MutableMapping[str, Any]] = None, fmt: Optional[str] = None):
        if not extra:
            extra = {}

        self.extra: MutableMapping[str, Any] = extra
        super().__init__(logger, extra=extra)
        if not fmt:
            fmt = ''
        self.fmt = fmt

    def _prettify_json(self, *record_fields, indent: int = 4) -> None:
        for el in record_fields:
            self.extra[el] = json.dumps(self.extra[el], indent=indent)


class RequestsAdapter(BaseAdapter):
    def __init__(self, logger: Logger, extra: Optional[dict] = None, fmt: Optional[str] = REQUESTS_MSG_FORMAT, log_type: str = 'request'):
        super().__init__(logger, extra=extra, fmt=fmt)
        self.log_type = log_type

    def process(self, msg: Any, kwargs: MutableMapping[str, Any]) -> tuple[Any, MutableMapping[str, Any]]:
        params: str = ' '.join(f'{param}={value}' for param, value in self.extra.items())
        message = self.fmt % {'params': params, 'msg': msg, 'type': self.log_type}
        return message, kwargs


class ErrorAdapter(BaseAdapter):
    def __init__(self, logger: Logger, extra: Optional[dict] = None, fmt: Optional[str] = ERROR_MSG_FORMAT):
        super().__init__(logger, extra=extra, fmt=fmt)

    def process(self, msg: Any, kwargs: MutableMapping[str, Any]) -> tuple[Any, MutableMapping[str, Any]]:
        self.extra['msg'] = msg
        message = self.fmt % self.extra
        return message, kwargs
