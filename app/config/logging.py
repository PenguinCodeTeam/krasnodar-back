import logging

from config import LOG_PROPAGATE, LOG_DIR, LOG_LEVEL


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '[%(asctime)s.%(msecs)03d] %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'},
        'console': {'format': '[%(asctime)s.%(msecs)03d] %(name)s:%(levelname)s %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'},
    },
    'filters': {
        'request_id_filter': {
            '()': 'internal.core.logs.filters.RequestIdFilter',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'formatter': 'console',
            'class': 'logging.StreamHandler',
        },
        'access_file_handler': {
            'formatter': 'standard',
            'level': logging.INFO,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'{LOG_DIR}/access.log',
            'when': 'midnight',
            'backupCount': 0,
        },
        'error_file_handler': {
            'formatter': 'standard',
            'level': logging.ERROR,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'{LOG_DIR}/error.log',
            'when': 'midnight',
            'backupCount': 0,
        },
        'requests_file_handler': {
            'formatter': 'standard',
            'level': logging.INFO,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': f'{LOG_DIR}/requests.log',
            'when': 'midnight',
            'backupCount': 0,
        },
    },
    'loggers': {
        'root': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['requests_file_handler'],
            'filters': ['request_id_filter'],
            'propagate': LOG_PROPAGATE,
        },
        'error': {
            'handlers': ['error_file_handler'],
            'filters': ['request_id_filter'],
            'level': logging.ERROR,
            'propagate': True,
        },
        'uvicorn': {'propagate': True},
        'uvicorn.error': {
            'handlers': ['error_file_handler'],
            'filters': [],
            'propagate': True,
        },
        'uvicorn.access': {
            'handlers': ['access_file_handler'],
            'filters': ['request_id_filter'],
            'level': logging.INFO,
            'propagate': True,
        },
    },
}
