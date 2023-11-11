from datetime import date
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import PriorityEnum, TaskStatusEnum, WorkerGradeEnum


class IdModel(BaseModel):
    id: UUID


class Point(BaseModel):
    id: UUID
    address: str
    city: str


class Employee(BaseModel):
    grade: WorkerGradeEnum
    name: str
    surname: str
    patronymic: str


class Task(BaseModel):
    id: UUID
    status: TaskStatusEnum
    name: str
    priority: PriorityEnum
    time: int
    point: Point
    date: date
    employee: Employee


class DestinationDataRow(BaseModel):
    connected_at: str | None = None
    is_delivered: bool | None = None
    days_after_delivery: int | None = None
    accepted_requests: int | None = None
    completed_requests: int | None = None


class DestinationDataRowRequest(DestinationDataRow):
    address: str


class DestinationDataRowResponse(DestinationDataRow):
    full_address: str


class TaskTypeDataRow(BaseModel):
    name: str
    priority: PriorityEnum
    duration: int
    grades: list[WorkerGradeEnum]


class WorkplaceDataRowResponse(BaseModel):
    full_address: str


class WorkerDataRow(BaseModel):
    name: str
    surname: str
    patronymic: str
    grade: WorkerGradeEnum
    login: str | None = None
    password: str | None = None


class WorkerDataRowRequest(WorkerDataRow):
    city: str
    address: str


class WorkerDataRowResponse(WorkerDataRow):
    full_address: str


class WorkScheduleResponse(BaseModel):
    full_address: str
    task_number: int
    date: date
    expected_start_at: int
    expected_finish_at: int
    started_at: int | None = None
    finished_at: int | None = None
