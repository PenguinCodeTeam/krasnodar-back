from pydantic import BaseModel

from internal.api.v1.schemas.common import IdModel
from internal.core.types import RoleEnum


class CheckAuthResponse(BaseModel):
    status: str = 'OK'


class LoginResponse(IdModel):
    access_token: str
    name: str
    surname: str
    patronymic: str
    role: RoleEnum
