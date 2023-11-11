from uuid import UUID

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.manager import CreateManagerRequest, UpdateManagerRequest
from internal.api.v1.schemas.response.manager import CreateManagerResponse, GetManagerResponse, GetManagersResponse
from internal.core.dependencies.authorization import ManagerAuthorize
from internal.services.user import UserService


MANAGER_ROUTER = APIRouter(prefix='/manager', tags=['Manager'], dependencies=[Depends(ManagerAuthorize())])


@MANAGER_ROUTER.get('/{user_id}')
async def get_manager_handler(user_id: UUID, service: UserService = Depends()) -> GetManagerResponse:
    """Получение информации о менеджере по id"""
    data = await service.get_manager(user_id)
    return GetManagerResponse.model_validate(data)


@MANAGER_ROUTER.get('')
async def get_managers_handler(service: UserService = Depends()) -> GetManagersResponse:
    """Получение всех менеджеров"""
    data = await service.get_managers()
    return GetManagersResponse(managers=data)


@MANAGER_ROUTER.post('')
async def create_manager_handler(request_data: CreateManagerRequest, service: UserService = Depends()) -> CreateManagerResponse:
    """Создание нового менеджера"""
    created_manager_id = await service.create_manager(**request_data.model_dump())
    return CreateManagerResponse(id=created_manager_id)


@MANAGER_ROUTER.patch('/{user_id}')
async def update_manager_handler(user_id: UUID, request_data: UpdateManagerRequest, service: UserService = Depends()) -> None:
    """Изменение информации о менеджере"""
    await service.update_manager(user_id, **request_data.model_dump(exclude_none=True))


@MANAGER_ROUTER.delete('/{user_id}')
async def delete_manager_handler(user_id: UUID, service: UserService = Depends()) -> None:
    """Удаление менеджера"""
    await service.delete_manager(user_id)
