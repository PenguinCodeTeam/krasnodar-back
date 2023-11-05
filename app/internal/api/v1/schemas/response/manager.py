from pydantic import BaseModel

from internal.api.v1.schemas.common import IdModel, InputDataRow
from internal.core.types import RoleEnum


class GetManagerResponse(IdModel):
    login: str
    name: str
    surname: str
    patronymic: str
    role: RoleEnum


class GetManagersResponse(BaseModel):
    managers: list[GetManagerResponse]


class GetInputDataResponse(BaseModel):
    input_data: list[InputDataRow]


class CreateManagerResponse(IdModel):
    pass
