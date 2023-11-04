from datetime import timedelta
from uuid import UUID

from pydantic import BaseModel

from internal.api.v1.schemas.common import EmployeeUser
from internal.core.types import PriorityEnum


class Point(BaseModel):
    latitude: float
    longitude: float


class Task(BaseModel):
    id: UUID
    name: str
    priority: PriorityEnum
    time: timedelta
    point: Point


class GetEmployeeTasksResponse(BaseModel):
    tasks: list[Task]


class GetEmployeeInfo(EmployeeUser):
    pass


class GetEmployeeUserResponse(EmployeeUser):
    pass
