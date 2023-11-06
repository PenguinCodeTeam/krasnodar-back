from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import RoleEnum, WorkerGradeEnum


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


class UpdateUserRequest(BaseModel):
    login: Optional[str]
    password: Optional[str]
    role: Optional[RoleEnum]
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    address: Optional[str]
    grade: Optional[WorkerGradeEnum]
