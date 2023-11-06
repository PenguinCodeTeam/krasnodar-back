from uuid import UUID

from fastapi import APIRouter, Body, Depends

from internal.api.v1.schemas.request.employee import CreateEmployeeUserRequest, UpdateUserRequest
from internal.api.v1.schemas.response.employee import CreateEmployeeResponse, GetEmployeeResponse, GetEmployeesResponse
from internal.core.dependencies.authorization import ManagerAuthorize, OnlyCurrentEmployeeAuthorize
from internal.services.user import UserService


EMPLOYEE_ROUTER = APIRouter(prefix='/employee', tags=['Employee'])


@EMPLOYEE_ROUTER.get('/', tags=['Working'], dependencies=[Depends(ManagerAuthorize())])
async def get_all_employees_handler(service: UserService = Depends()) -> GetEmployeesResponse:
    """Получение всех сотрудников. Для менеджера"""
    data = await service.get_employees()
    return GetEmployeesResponse(employees=data)


@EMPLOYEE_ROUTER.post('/', tags=['Working'], dependencies=[Depends(ManagerAuthorize())])
async def create_employee_handler(request_data: CreateEmployeeUserRequest = Body(), service: UserService = Depends()) -> CreateEmployeeResponse:
    """Создание профиля работника. Для менеджера"""
    data = await service.create_employee(**request_data.model_dump())
    return CreateEmployeeResponse(id=data)


@EMPLOYEE_ROUTER.get('/{user_id}', tags=['Working'], dependencies=[Depends(OnlyCurrentEmployeeAuthorize())])
async def get_employee_handler(user_id: UUID, service: UserService = Depends()) -> GetEmployeeResponse:
    """Получение информации о работнике по id. Для менеджера и работника для получения информации о себе"""
    data = await service.get_employee(user_id)
    return GetEmployeeResponse.model_validate(data)


@EMPLOYEE_ROUTER.patch('/{user_id}', dependencies=[Depends(ManagerAuthorize())])
async def update_employee_handler(user_id: UUID, request_data: UpdateUserRequest = Body()):
    """Обновление профиля работнике. Для менеджера"""
    return None
