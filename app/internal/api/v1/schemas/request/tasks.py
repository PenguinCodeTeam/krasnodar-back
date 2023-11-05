from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import TaskStatusEnum


class GetTasksRequest(BaseModel):
    user_id: Optional[UUID]
    date: date


class UpdateTaskRequest(BaseModel):
    status: TaskStatusEnum
    message: str
