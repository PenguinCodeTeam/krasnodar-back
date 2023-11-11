import datetime

from fastapi import APIRouter, Body, Depends

from internal.api.v1.schemas.request.manager import SetInputDataRequest
from internal.api.v1.schemas.response.manager import GetInputDataResponse
from internal.core.dependencies.authorization import ManagerAuthorize
from internal.services.input_data import InputDataService


INPUT_ROUTER = APIRouter(tags=['Input'], dependencies=[Depends(ManagerAuthorize())])


@INPUT_ROUTER.get('/input_data')
async def get_input_data(service: InputDataService = Depends(), date: datetime.date | None = None) -> GetInputDataResponse:
    """Получение текущих входных данных"""
    if date is None:
        date = datetime.date.today()
    response = await service.get_input_data(date)
    return GetInputDataResponse.model_validate(response)


@INPUT_ROUTER.post('/input_data')
async def set_input_data_handler(request_data: SetInputDataRequest = Body(), service: InputDataService = Depends()) -> GetInputDataResponse:
    """Загрузка или изменение входных данных для дальнейшего распределения задач"""
    data = request_data.model_dump()
    response = await service.set_input_data(destinations=data['destinations'], city=data['city'])
    return GetInputDataResponse.model_validate(response)
