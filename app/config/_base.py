import os


APP_URL_PREFIX = ''
APP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__) or '.'))
DEBUG = False
INSTANCE_ID = os.environ.get('INSTANCE_ID') or os.environ.get('HOSTNAME') or ''
SERVER_HOST = '0.0.0.0'
SERVER_PORT = '7070'
LOG_PROPAGATE = False
LOG_DIR = os.path.normpath(f'{os.path.dirname(__file__)}/../../logs')
LOG_LEVEL = 'INFO'
CHECK_CONFIG = False
MASKING_ENABLED = False
MASKS = {
    'login': None,
    'password': None,
    'message': {'start': '50%'},
    'phone': {'start': 4, 'end': 2},
    'code': {'end': '50%'},
}
MASK_LENGTH = 8
