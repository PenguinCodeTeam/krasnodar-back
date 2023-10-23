import logging
import traceback
from typing import NotRequired, TypedDict, Unpack

from fastapi.requests import Request

import config
from internal.core.logs.adapters import ErrorAdapter, RequestsAdapter


ERROR_LOGGER = logging.getLogger('error')
REQUESTS_LOGGER = logging.getLogger('requests')


class RequestsLogData(TypedDict):
    route: str
    body: dict
    query: NotRequired[dict]
    log_type: NotRequired[str]


def exc_to_log(request: Request):
    tb = traceback.format_exc(chain=False)
    tb = ''.join(tb).replace('^', '')

    error_adapter = ErrorAdapter(ERROR_LOGGER, extra={'traceback': tb})
    error_adapter.error('')

    extra = {
        'route': request.url.path,
        'client': request.client.host,  # type: ignore
        'headers': dict(request.headers.items()),
    }
    adapter = RequestsAdapter(REQUESTS_LOGGER, extra=extra, log_type='error')
    adapter.info('')


def log_requests(**kwargs: Unpack[RequestsLogData]):
    if kwargs.get('query') is None:
        kwargs['query'] = {}
    log_type = kwargs.pop('log_type')
    if config.MASKING_ENABLED:
        body = kwargs.get('body')
        if isinstance(body, dict):
            kwargs['body'] = mask_data(body)
    if log_type == 'response':
        kwargs.pop('query')
    adapter = RequestsAdapter(REQUESTS_LOGGER, extra=kwargs, log_type=log_type)
    adapter.info('')


def mask_data(data: dict) -> dict:
    mask = {}
    for item, value in data.items():
        if item in config.MASKS:
            mask[item] = apply_mask(value, config.MASKS.get(item))
        else:
            mask[item] = value
    return mask


def apply_mask(value: str, rule: dict):
    """Применение маски к значению
    Args:
        value: Значение параметра для маскирования
        rule: Правило для маскирования
    Returns:
        маскированная строка
    """
    if not isinstance(rule, dict):
        return '*' * config.MASK_LENGTH
    start = rule.get('start')
    end = rule.get('end')
    try:
        if isinstance(start, int) and isinstance(end, int):
            return value[:start] + '*' * max(0, len(value) - start - end) + value[-end:]
        elif isinstance(start, str) and '%' in start:
            start = int(len(value) * int(start.replace('%', '')) / 100)
            return '*' * max(0, len(value) - start) + value[start:]
        elif isinstance(end, str) and '%' in end:
            end = int(len(value) * int(end.replace('%', '')) / 100)
            return value[:-end] + '*' * max(0, len(value) - end)
    except (IndexError, TypeError):
        return '*' * len(value)
