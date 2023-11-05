from pydantic import BaseModel

from internal.api.v1.schemas.common import EmployeeUser, Task


class GetEmployeeTasksResponse(BaseModel):
    tasks: list[Task]


class GetEmployeesResponse(BaseModel):
    employees: list[EmployeeUser]


class GetEmployeeResponse(EmployeeUser):
    pass
