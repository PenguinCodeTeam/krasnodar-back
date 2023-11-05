from uuid import UUID

from pydantic import BaseModel

from internal.core.types import RoleEnum


class CheckAuthResponse(BaseModel):
    status: str = 'OK'


class LoginResponse(BaseModel):
    access_token: str
    name: str
    surname: str
    patronymic: str
    role: RoleEnum
    id: UUID
