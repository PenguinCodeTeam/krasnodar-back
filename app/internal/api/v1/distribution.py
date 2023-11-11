import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.response.manager import GetTasksDistributionResponse, GetWorkerTasksDistributionResponse
from internal.core.dependencies.authorization import ManagerAuthorize, OnlyCurrentEmployeeAuthorize
from internal.services.distribution import DistributionService


DISTRIBUTION_ROUTER = APIRouter(tags=['Distribution'])


@DISTRIBUTION_ROUTER.post('/distribution', dependencies=[Depends(ManagerAuthorize())])
async def start_distribution_handler(service: DistributionService = Depends()) -> GetTasksDistributionResponse:
    """Запуск распределения задач"""
    response = await service.start_distribution()
    return GetTasksDistributionResponse.model_validate(response)


@DISTRIBUTION_ROUTER.get('/distribution', dependencies=[Depends(ManagerAuthorize())])
async def get_distribution_status_handler(service: DistributionService = Depends(), date: datetime.date | None = None) -> GetTasksDistributionResponse:
    """Получение статуса состояния распределения задач"""
    if date is None:
        date = datetime.date.today()
    response = await service.get_distribution_results(date)
    return GetTasksDistributionResponse.model_validate(response)


@DISTRIBUTION_ROUTER.get('/distribution/{user_id}', dependencies=[Depends(OnlyCurrentEmployeeAuthorize())])
async def get_distribution_status_handler_by_user(
    user_id: UUID, service: DistributionService = Depends(), date: datetime.date | None = None
) -> GetWorkerTasksDistributionResponse:
    """Получение статуса состояния распределения задач по пользователю"""
    if date is None:
        date = datetime.date.today()
    response = await service.get_distribution_result(user_id, date)
    return GetWorkerTasksDistributionResponse.model_validate(response)
