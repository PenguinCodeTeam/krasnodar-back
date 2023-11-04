from typing import Optional

from pydantic import BaseModel

from internal.api.v1.schemas.common import User
from internal.core.types import RoleEnum


class InputDataRow(BaseModel):
    address: str
    connected_at: str
    is_delivered: bool
    days_after_delivery: int
    accepted_requests: int
    completed_requests: int


class SetInputDataRequest(BaseModel):
    input_data: list[InputDataRow]


class CreateManagerRequest(User):
    role: RoleEnum = RoleEnum.MANAGER


class UpdateManagerRequest(BaseModel):
    login: Optional[str]
    password: Optional[str]
    role: Optional[RoleEnum] = RoleEnum.MANAGER
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
