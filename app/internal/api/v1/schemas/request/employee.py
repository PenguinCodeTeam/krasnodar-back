from uuid import UUID

from pydantic import BaseModel

from internal.core.types import WorkerGradeEnum


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
    city: str = 'Краснодар'
    address: str
    grade: WorkerGradeEnum


class UpdateEmployeeRequest(BaseModel):
    login: str = None
    password: str = None
    name: str = None
    surname: str = None
    patronymic: str = None
    workplace_id: UUID = None
    grade: WorkerGradeEnum = None
