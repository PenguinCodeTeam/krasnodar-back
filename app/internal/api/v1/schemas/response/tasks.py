from pydantic import BaseModel

from internal.api.v1.schemas.common import Task


class GetTaskResponse(Task):
    pass


class GetAllTasksResponse(BaseModel):
    tasks: list[Task]
