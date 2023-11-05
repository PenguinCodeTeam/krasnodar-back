from uuid import UUID

from fastapi import APIRouter, Body

from internal.api.v1.schemas.request.manager import CreateManagerRequest, SetInputDataRequest, UpdateManagerRequest
from internal.api.v1.schemas.response.manager import GetInputDataResponse, GetManagerResponse


MANAGER_ROUTER = APIRouter(prefix='/manager', tags=['Manager'])


@MANAGER_ROUTER.get('/input_data')
async def get_input_data() -> GetInputDataResponse:
    """Получение текущих входных данных"""
    pass


@MANAGER_ROUTER.post('/input_data')
async def set_input_data_handler(request_data: SetInputDataRequest = Body()) -> None:
    """Загрузка или изменение входных данных для дальнейшего распределения задач"""
    return None


@MANAGER_ROUTER.post('/distribution')
async def start_distribution_handler() -> None:
    """Запуск распределения задач"""
    return None


@MANAGER_ROUTER.get('/distribution')
async def get_distribution_status_handler() -> None:
    """Получение статуса состояния распределения задач"""
    return None


@MANAGER_ROUTER.get('/{user_id}')
async def get_manager_handler(user_id) -> GetManagerResponse:
    """Получение информации о менеджере по id"""
    return GetManagerResponse()


@MANAGER_ROUTER.post('/')
async def create_manager_handler(request_data: CreateManagerRequest) -> None:
    """Создание нового менеджера"""
    return None


@MANAGER_ROUTER.patch('/{user_id}')
async def update_manager_handler(user_id: UUID, request_data: UpdateManagerRequest) -> None:
    """Изменение информации о менеджере"""
    return None
