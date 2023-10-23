import logging
import os
from logging.config import dictConfig

from config.logging import LOGGING
from internal.core.requests import request_id_var


def check_entry(log_file_path):
    assert os.path.exists(log_file_path)
    result = {'username': False, 'req_id': False}
    with open(log_file_path, 'r') as file:
        for line in file:
            if line.strip() == '"req_id": "#RANDOMidD3o_d",':
                result['req_id'] = True
            if line.strip() == '"username": "-",':
                result['username'] = True
            if all(result.values()):
                return True

    return False


def check_entry_username(log_file_path):
    assert os.path.exists(log_file_path)
    with open(log_file_path, 'r') as file:
        for line in file:
            if line.strip() == '"username": "usertest",':
                return True

    return False


def configure_logger(filepath: str) -> logging.Logger:
    LOGGING['handlers']['access_file_handler']['filename'] = filepath
    dictConfig(LOGGING)
    return logging.getLogger('access')


def test_access_logger(tmp_path):
    request_id_var.set('RANDOMidD3o_d')
    filepath = os.path.join(tmp_path, 'access.log')
    configure_logger(filepath)

    test_data = '127.0.0.1:56698 - "GET /notifications/v1/clients/fkjadsf HTTP/1.1" 422'

    access_logger = logging.getLogger('uvicorn.access')
    access_logger.info(test_data)
    assert os.path.exists(filepath)

    with open(filepath, 'r') as f:
        content = f.read()
        assert test_data in content
