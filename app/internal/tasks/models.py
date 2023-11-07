from uuid import UUID

from pydantic import BaseModel

from app.internal.core.types import PriorityEnum


class Point(BaseModel):
    id: UUID
    address: str
    latitude: float
    longitude: float


class Task(BaseModel):
    point: Point
    priority: PriorityEnum
    duration_work: int


class GradeTasks(BaseModel):
    senior: list[Task]
    middle: list[Task]
    junior: list[Task]


class GraphElement(BaseModel):
    duration: int
    task: Task
