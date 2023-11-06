from typing import Optional, Type
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import Empty, WorkerGradeEnum


class FinishTaskRequest(BaseModel):
    comment: str


class GetEmployeeRequest(BaseModel):
    grade: WorkerGradeEnum


class CreateEmployeeUserRequest(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    patronymic: str
    workplace_id: UUID
    grade: WorkerGradeEnum


class UpdateEmployeeRequest(BaseModel):
    login: Optional[str | Type] = Empty
    password: Optional[str | Type] = Empty
    name: Optional[str | Type] = Empty
    surname: Optional[str | Type] = Empty
    patronymic: Optional[str | Type] = Empty
    workplace_id: Optional[UUID | Type] = Empty
    grade: Optional[WorkerGradeEnum | Type] = Empty
