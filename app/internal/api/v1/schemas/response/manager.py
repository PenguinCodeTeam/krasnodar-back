from typing import Any

from pydantic import BaseModel

from internal.api.v1.schemas.common import (
    DestinationDataRowResponse,
    IdModel,
    TaskTypeDataRow,
    WorkerDataRowResponse,
    WorkplaceDataRowResponse,
    WorkScheduleResponse,
)
from internal.core.types import CeleryTaskStatusEnum, RoleEnum


class GetManagerResponse(IdModel):
    login: str
    name: str
    surname: str
    patronymic: str
    role: RoleEnum


class GetManagersResponse(BaseModel):
    managers: list[GetManagerResponse]


class InputDataResult(BaseModel):
    success: int
    failed: int
    success_data: list[Any]
    failed_data: list[Any]


class DestinationDataResult(InputDataResult):
    success_data: list[DestinationDataRowResponse]
    failed_data: list[DestinationDataRowResponse]


class TaskTypeDataResult(InputDataResult):
    success_data: list[TaskTypeDataRow]
    failed_data: list[TaskTypeDataRow]


class WorkplaceDataResult(InputDataResult):
    success_data: list[WorkplaceDataRowResponse]
    failed_data: list[WorkplaceDataRowResponse]


class WorkerDataResult(InputDataResult):
    success_data: list[WorkerDataRowResponse]
    failed_data: list[WorkerDataRowResponse]


class DestinationDataResults(BaseModel):
    new: DestinationDataResult
    updated: DestinationDataResult


class TaskTypeDataResults(BaseModel):
    new: TaskTypeDataResult
    updated: TaskTypeDataResult


class WorkplaceDataResults(BaseModel):
    new: WorkplaceDataResult
    updated: WorkplaceDataResult


class WorkerDataResults(BaseModel):
    new: WorkerDataResult
    updated: WorkerDataResult


class InputDataResponse(BaseModel):
    destinations: DestinationDataResults
    task_types: TaskTypeDataResults
    workplaces: WorkplaceDataResults
    workers: WorkerDataResults


class CeleryTaskResponse(BaseModel):
    status: CeleryTaskStatusEnum
    result: Any | None = None


class GetInputDataResponse(CeleryTaskResponse):
    result: InputDataResponse | None = None


class TasksDistributionWorkerResponse(BaseModel):
    worker: WorkerDataRowResponse
    tasks: list[WorkScheduleResponse]


class TasksDistributionResponse(BaseModel):
    workers_distribution: list[TasksDistributionWorkerResponse]


class GetTasksDistributionResponse(CeleryTaskResponse):
    result: TasksDistributionResponse | None = None


class CreateManagerResponse(IdModel):
    pass
