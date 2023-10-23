import config


config.DEBUG = False
config.CHECK_CONFIG = True
config.MASKING_ENABLED = True
config.MASKS = {
    'login': None,
    'password': None,
    'message': {'start': '50%'},
    'phone': {'start': 4, 'end': 2},
    'code': {'end': '50%'},
}
config.MASK_LENGTH = 8
