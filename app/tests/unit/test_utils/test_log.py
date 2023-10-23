import logging
from copy import deepcopy
from logging.config import dictConfig

from config.logging import LOGGING
from internal.core.logs.helpers import mask_data


def configure_loggers(logging_dict: dict, propagate: bool = False):
    ld = deepcopy(logging_dict)

    for logger in ld['loggers']:
        if logger != 'root':
            ld['loggers'][logger]['handlers'] = []
            ld['loggers'][logger]['propagate'] = propagate
    dictConfig(ld)


def test_log_to_stderr(capsys):
    configure_loggers(LOGGING, propagate=True)
    test_message = 'sens3lesst3%sdtText'

    logger = logging.getLogger('requests')
    logger.info(test_message)

    captured = capsys.readouterr()
    assert test_message in captured.err


def test_no_log_to_stderr(capsys):
    configure_loggers(LOGGING, propagate=False)
    test_message = 'anotherText'

    logger = logging.getLogger('requests')
    logger.info(test_message)

    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err


def test_none_value(data):
    result = mask_data(data)
    assert result['login'] == '********'
    assert result['password'] == '********'


def test_start_end_values(data):
    result = mask_data(data)
    assert result['message'] == '********90123456'
    assert result['phone'] == '+155******55'


def test_length_same_as_input(data):
    result = mask_data(data)
    assert len(result['message']) == len(data['message'])
    assert len(result['phone']) == len(data['phone'])
    assert len(result['login']) == 8
    assert len(result['code']) == len(data['code'])


def test_error_handling():
    invalid_data = {
        'message': {1234567890123456},
        'phone': ['+15555555555'],
        'login': ['test@example.com'],
        'code': {423423, 'fdsfsd'},
    }
    result = mask_data(invalid_data)
    assert result == {'code': '**', 'login': '********', 'message': '*', 'phone': '*'}
