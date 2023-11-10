import datetime

from pydantic import BaseModel

from internal.api.v1.schemas.common import DestinationDataRowRequest, TaskTypeDataRow, WorkerDataRowRequest


class SetInputDataRequest(BaseModel):
    date: datetime.date
    destinations: list[DestinationDataRowRequest]
    task_types: list[TaskTypeDataRow]
    workers: list[WorkerDataRowRequest]


class CreateManagerRequest(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    patronymic: str


class UpdateManagerRequest(BaseModel):
    login: str = None
    password: str = None
    name: str = None
    surname: str = None
    patronymic: str = None
