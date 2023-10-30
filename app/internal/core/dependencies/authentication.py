from fastapi import HTTPException, Request

import config
from internal.core.exceptions import AccessForbiddenException, ExpiredTokenException, InvalidTokenException
from internal.services.authentication.jwt import decode_jwt


class BaseAuthorize:
    """Базовый класс зависимости авторизации FA для JWT Авторизации"""

    async def __call__(self, request: Request):
        if config.DEBUG:
            return

        raw_token = request.headers.get('Authorization')

        if not raw_token:
            raise HTTPException(status_code=401, detail='Token is empty')

        splited_token = raw_token.split()
        if not splited_token or len(splited_token) != 2:
            raise HTTPException(status_code=401, detail='Invalid token')

        auth_type, token = raw_token.split(' ')

        if auth_type != 'Bearer':
            raise HTTPException(status_code=401, detail=f'Invalid authentication type {auth_type}')

        try:
            payload = decode_jwt(token)
        except InvalidTokenException as e:
            raise HTTPException(status_code=401, detail='Invalid token') from e
        except ExpiredTokenException as e:
            raise HTTPException(status_code=401, detail='Token expired') from e

        try:
            await self.has_access(payload.get('login'))
        except AccessForbiddenException as e:
            raise HTTPException(status_code=403, detail='Access restricted') from e

    async def has_access(self, login: str):
        raise NotImplementedError()


class EmployeeAuthorize(BaseAuthorize):
    async def has_access(self, login: str) -> bool:
        return login == 'test'


class ManagerAuthorize(BaseAuthorize):
    async def has_access(self, login: str) -> bool:
        return login == 'manager'
