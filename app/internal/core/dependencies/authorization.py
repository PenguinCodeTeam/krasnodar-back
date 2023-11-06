from typing import Iterable
from uuid import UUID

from fastapi import HTTPException, Request

import config
from internal.core.exceptions import AccessForbiddenException, ExpiredTokenException, InvalidTokenException
from internal.core.types.users import RoleEnum
from internal.repositories.db.users import UserRepository
from internal.services.authentication.jwt import decode_jwt


class BaseAuthorize:
    """Базовый класс зависимости авторизации FA для JWT Авторизации"""

    def __init__(self):
        self.repository = UserRepository()

    async def __call__(self, request: Request):
        if not config.DEBUG:
            await self.validate(request)

    async def validate(self, request: Request):
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
            self.payload = decode_jwt(token)
        except InvalidTokenException as e:
            raise HTTPException(status_code=401, detail='Invalid token') from e
        except ExpiredTokenException as e:
            raise HTTPException(status_code=401, detail='Token expired') from e

    async def _check_access(self, user_id: UUID, expected_roles: Iterable[RoleEnum]):
        user = await self.repository.get_user(user_id=user_id)
        if user.role not in expected_roles:
            raise AccessForbiddenException()


class EmployeeAuthorize(BaseAuthorize):
    async def validate(self, request: Request):
        await super().validate(request)
        try:
            await self._check_access(self.payload.get('user_id'), (RoleEnum.EMPLOYEE, RoleEnum.MANAGER))
        except AccessForbiddenException as e:
            raise HTTPException(status_code=403, detail='Access restricted') from e


class OnlyCurrentEmployeeAuthorize(BaseAuthorize):
    async def __call__(self, request: Request, user_id: UUID):
        if not config.DEBUG:
            await self.validate(request, user_id)

    async def validate(self, request: Request, user_id: UUID):
        await super().validate(request)
        user = await self.repository.get_user(self.payload.get('user_id'))

        if user.role == RoleEnum.EMPLOYEE:
            if user.id != user_id:
                raise HTTPException(status_code=403, detail='Access restricted')


class ManagerAuthorize(BaseAuthorize):
    async def validate(self, request: Request):
        await super().validate(request)
        try:
            await self._check_access(self.payload.get('user_id'), (RoleEnum.MANAGER,))
        except AccessForbiddenException as e:
            raise HTTPException(status_code=403, detail='Access restricted') from e
