from datetime import date
from uuid import UUID

from pydantic import BaseModel

from internal.core.types import PriorityEnum, TaskStatusEnum, WorkerGradeEnum


class GetTasksRequest(BaseModel):
    grade: WorkerGradeEnum | None = None
    priority: PriorityEnum | None = None
    status: TaskStatusEnum | None = None
    task_type_id: UUID | None = None


class GetAppointedTasksRequest(BaseModel):
    grade: WorkerGradeEnum | None = None
    priority: PriorityEnum | None = None
    status: TaskStatusEnum | None = None
    user_id: UUID | None = None
    date: date


class UpdateAppointedTaskRequest(BaseModel):
    status: TaskStatusEnum
    message: str
