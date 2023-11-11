from pydantic import BaseModel

from internal.api.v1.schemas.common import IdModel, Point
from internal.core.types import RoleEnum, WorkerGradeEnum


class GetEmployeeResponse(IdModel):
    workplace: Point
    login: str
    grade: WorkerGradeEnum
    name: str
    surname: str
    patronymic: str
    role: RoleEnum


class GetEmployeesResponse(BaseModel):
    employees: list[GetEmployeeResponse]


class CreateEmployeeResponse(IdModel):
    pass
