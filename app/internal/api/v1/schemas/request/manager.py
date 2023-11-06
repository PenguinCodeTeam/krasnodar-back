from typing import Optional, Type

from pydantic import BaseModel

from internal.api.v1.schemas.common import InputDataRow
from internal.core.types import Empty


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
    login: Optional[str | Type] = Empty
    password: Optional[str | Type] = Empty
    name: Optional[str | Type] = Empty
    surname: Optional[str | Type] = Empty
    patronymic: Optional[str | Type] = Empty
