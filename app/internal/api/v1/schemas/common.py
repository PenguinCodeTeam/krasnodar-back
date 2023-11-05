from datetime import date
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import PriorityEnum, RoleEnum, TaskStatusEnum


class User(BaseModel):
    login: str
    role: RoleEnum
    name: str
    surname: str
    patronymic: str


class EmployeeUser(User):
    role: RoleEnum = RoleEnum.EMPLOYEE
    address: str
    grade: str


class Point(BaseModel):
    latitude: float
    longitude: float


class Task(BaseModel):
    id: UUID
    status: TaskStatusEnum
    name: str
    priority: PriorityEnum
    time: int
    point: Point
    date: date
    employee_id: UUID


class InputDataRow(BaseModel):
    address: str
    connected_at: str
    is_delivered: bool
    days_after_delivery: int
    accepted_requests: int
    completed_requests: int
