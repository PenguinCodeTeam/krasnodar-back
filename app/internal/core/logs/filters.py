from logging import Filter, LogRecord


class RequestIdFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        req_id = getattr(record, 'req_id', '-')
        record.msg = f'{req_id} {record.msg}'
        return True
