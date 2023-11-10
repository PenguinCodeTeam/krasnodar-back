import datetime
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import PriorityEnum, TaskStatusEnum


class Point(BaseModel):
    id: UUID
    full_address: str


class AppointedTask(BaseModel):
    id: UUID
    status: TaskStatusEnum
    name: str
    priority: PriorityEnum
    time: int
    point: Point
    created_date: datetime.date
    date: datetime.date
    task_number: int
    started_at: str
    finished_at: str
    message: str


class GetAppointedAppointedTaskResponse(AppointedTask):
    pass


class GetAppointedTasksResponse(BaseModel):
    tasks: list[AppointedTask]
