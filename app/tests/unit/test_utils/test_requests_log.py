import logging
import os
from logging.config import dictConfig
from unittest.mock import patch
from urllib.parse import urljoin

import pytest

import config
from config.logging import LOGGING
from internal.core.logs.adapters import RequestsAdapter
from internal.core.logs.helpers import log_requests
from internal.core.requests import request_id_var


def configure_logger(filepath: str) -> logging.Logger:
    LOGGING['handlers']['requests_file_handler']['filename'] = filepath
    dictConfig(LOGGING)

    return logging.getLogger('requests')


def test_requests_logger(tmp_path, caplog):
    request_id_var.set('RANDOMidD3o_d')
    filepath = os.path.join(tmp_path, 'requests.log')
    configure_logger(filepath)

    test_data = {'route': urljoin(config.APP_URL_PREFIX, '/api/status'), 'query': {'lang': 'ru'}, 'body': {'name': 'empty'}, 'log_type': 'request'}

    log_requests(**test_data)

    assert os.path.exists(filepath)

    with open(filepath, 'r') as file:
        content = file.read()
        for v in test_data.values():
            assert str(v) in content


def test_response_logger(tmp_path, caplog):
    request_id_var.set('RANDOMidD3o_d')
    filepath = os.path.join(tmp_path, 'requests.log')
    configure_logger(filepath)

    test_data = {'route': urljoin(config.APP_URL_PREFIX, '/api/status'), 'body': {'is_success': True, 'data': {'status': 'ok'}}, 'log_type': 'response'}
    log_requests(**test_data)

    assert os.path.exists(filepath)

    with open(filepath, 'r') as file:
        content = file.read()
        for v in test_data.values():
            assert str(v) in content


@pytest.mark.asyncio
async def test_requests_logging_middleware(client, tmp_path):
    logger = logging.getLogger('requests')
    logger.handlers = []
    with patch.object(RequestsAdapter, 'info') as mock_info:

        response = client.get(
            urljoin(config.APP_URL_PREFIX, '/api/status'), params={'lang': 'ru'}
        )
        assert response.status_code == 200

        mock_info.assert_called()
