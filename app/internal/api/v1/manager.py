from uuid import UUID

from fastapi import APIRouter, Body, Depends

from internal.api.v1.schemas.request.manager import CreateManagerRequest, SetInputDataRequest, UpdateManagerRequest
from internal.api.v1.schemas.response.manager import CreateManagerResponse, GetInputDataResponse, GetManagerResponse, GetManagersResponse
from internal.core.dependencies.authentication import ManagerAuthorize
from internal.services.user import UserService


MANAGER_ROUTER = APIRouter(prefix='/manager', tags=['Manager'], dependencies=[Depends(ManagerAuthorize())])


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


@MANAGER_ROUTER.get('/{user_id}', tags=['Working'])
async def get_manager_handler(user_id: UUID, service: UserService = Depends()) -> GetManagerResponse:
    """Получение информации о менеджере по id"""
    data = await service.get_manager(user_id)
    return GetManagerResponse.model_validate(data)


@MANAGER_ROUTER.get('/', tags=['Working'])
async def get_managers_handler(service: UserService = Depends()) -> GetManagersResponse:
    """Получение всех менеджеров"""
    data = await service.get_managers()
    return GetManagersResponse(managers=data)


@MANAGER_ROUTER.post('/', tags=['Working'])
async def create_manager_handler(request_data: CreateManagerRequest, service: UserService = Depends()) -> CreateManagerResponse:
    """Создание нового менеджера"""
    data = await service.create_manager(**request_data.model_dump())
    return CreateManagerResponse(id=data)


@MANAGER_ROUTER.patch('/{user_id}')
async def update_manager_handler(user_id: UUID, request_data: UpdateManagerRequest) -> None:
    """Изменение информации о менеджере"""
    return None
