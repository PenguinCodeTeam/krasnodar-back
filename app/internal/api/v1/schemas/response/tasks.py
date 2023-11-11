import datetime
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import PriorityEnum, TaskStatusEnum


class Point(BaseModel):
    id: UUID
    full_address: str


class Task(BaseModel):
    id: UUID
    status: TaskStatusEnum
    name: str
    task_type_id: int
    priority: PriorityEnum
    time: int
    point: Point
    created_date: datetime.date


class GetTaskResponse(Task):
    pass


class GetTasksResponse(BaseModel):
    tasks: list[Task]


class AppointedTask(BaseModel):
    id: UUID
    status: TaskStatusEnum
    name: str
    task_type_id: int
    priority: PriorityEnum
    time: int
    point: Point
    created_date: datetime.date
    date: datetime.date
    task_number: int
    started_at: str
    finished_at: str
    message: str


class GetAppointedTaskResponse(AppointedTask):
    pass


class GetAppointedTasksResponse(BaseModel):
    tasks: list[AppointedTask]


class GetTaskTypeResponse(BaseModel):
    id: int
    name: str
    priority: PriorityEnum
    duration: int


class GetTaskTypesResponse(BaseModel):
    task_types: list[GetTaskTypeResponse]
