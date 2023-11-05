from pydantic import BaseModel

from internal.api.v1.schemas.common import EmployeeUser, Task


class GetEmployeeTasksResponse(BaseModel):
    tasks: list[Task]


class GetEmployeeInfo(EmployeeUser):
    pass


class GetAllEmployeesResponse(BaseModel):
    employees: list[EmployeeUser]


class GetEmployeeUserResponse(EmployeeUser):
    pass
