from typing import Optional

from pydantic import BaseModel

from internal.api.v1.schemas.common import InputDataRow
from internal.core.types import RoleEnum


class OptionalInputDataRow(BaseModel):
    address: Optional[str]
    connected_at: Optional[str]
    is_delivered: Optional[bool]
    days_after_delivery: Optional[int]
    accepted_requests: Optional[int]
    completed_requests: Optional[int]


class UpdateInputDataRequest(BaseModel):
    input_data: list[InputDataRow]


class SetInputDataRequest(BaseModel):
    input_data: list[InputDataRow]


class CreateManagerRequest(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    patronymic: str


class UpdateManagerRequest(BaseModel):
    login: Optional[str]
    password: Optional[str]
    role: Optional[RoleEnum] = RoleEnum.MANAGER
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
