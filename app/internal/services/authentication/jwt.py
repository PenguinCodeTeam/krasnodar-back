import datetime

import config
import jwt
from internal.core.exceptions import ExpiredTokenException, InvalidTokenException
from internal.services.authentication.helpers import form_token_due_date_lifetime


def encode_jwt(login: str, raw_token_lifetime=config.JWT_LIFETIME):
    payload = {'login': login, 'expiration': form_token_due_date_lifetime(raw_token_lifetime).strftime(config.JWT_EXP_DATE_FORMAT)}
    return jwt.encode(payload, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, key=config.JWT_SECRET, algorithms=config.JWT_ALGORITHM)
    except jwt.exceptions.PyJWTError:
        raise InvalidTokenException()

    if datetime.datetime.strptime(payload['expiration'], config.JWT_EXP_DATE_FORMAT) < datetime.datetime.now():
        raise ExpiredTokenException()

    return payload
