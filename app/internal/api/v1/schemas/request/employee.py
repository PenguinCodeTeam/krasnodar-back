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
    login: str | None = None
    password: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    address: str | None = None
    city: str | None = 'Краснодар'
    grade: WorkerGradeEnum | None = None
