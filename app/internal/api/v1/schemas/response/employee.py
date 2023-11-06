from pydantic import BaseModel

from internal.api.v1.schemas.common import IdModel, Point, Task
from internal.core.types import RoleEnum


class GetEmployeeTasksResponse(BaseModel):
    tasks: list[Task]


class GetEmployeeResponse(IdModel):
    workplace: Point
    login: str
    name: str
    surname: str
    patronymic: str
    role: RoleEnum


class GetEmployeesResponse(BaseModel):
    employees: list[GetEmployeeResponse]


class CreateEmployeeResponse(IdModel):
    pass
