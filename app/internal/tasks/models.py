from pydantic import BaseModel

from app.internal.core.types import PriorityEnum
from app.internal.repositories.db.models import Point


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
