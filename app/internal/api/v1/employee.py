from uuid import UUID

from fastapi import APIRouter, Body, Depends

from internal.api.v1.schemas.request.employee import CreateEmployeeUserRequest, UpdateEmployeeRequest
from internal.api.v1.schemas.response.employee import CreateEmployeeResponse, GetEmployeeResponse, GetEmployeesResponse
from internal.core.dependencies.authorization import ManagerAuthorize, OnlyCurrentEmployeeAuthorize
from internal.services.user import UserService


EMPLOYEE_ROUTER = APIRouter(prefix='/employee', tags=['Employee'])


@EMPLOYEE_ROUTER.get('/', dependencies=[Depends(ManagerAuthorize())])
async def get_all_employees_handler(service: UserService = Depends()) -> GetEmployeesResponse:
    """Получение всех сотрудников. Для менеджера"""
    data = await service.get_employees()
    return GetEmployeesResponse(employees=data)


@EMPLOYEE_ROUTER.post('/', dependencies=[Depends(ManagerAuthorize())])
async def create_employee_handler(request_data: CreateEmployeeUserRequest = Body(), service: UserService = Depends()) -> CreateEmployeeResponse:
    """Создание профиля работника. Для менеджера"""
    data = await service.create_employee(**request_data.model_dump())
    return CreateEmployeeResponse(id=data)


@EMPLOYEE_ROUTER.get('/{user_id}', dependencies=[Depends(OnlyCurrentEmployeeAuthorize())])
async def get_employee_handler(user_id: UUID, service: UserService = Depends()) -> GetEmployeeResponse:
    """Получение информации о работнике по id. Для менеджера и работника для получения информации о себе"""
    data = await service.get_employee(user_id)
    return GetEmployeeResponse.model_validate(data)


@EMPLOYEE_ROUTER.patch('/{user_id}', dependencies=[Depends(ManagerAuthorize())])
async def update_employee_handler(user_id: UUID, request_data: UpdateEmployeeRequest = Body(), service: UserService = Depends()):
    """Обновление профиля работнике. Для менеджера"""
    await service.update_employee(user_id, **request_data.model_dump())


@EMPLOYEE_ROUTER.delete('/{user_id}', dependencies=[Depends(ManagerAuthorize())])
async def delete_employee_handler(user_id: UUID, service: UserService = Depends()):
    """Удаление пролфиля работника. Для менеджера"""
    await service.delete_employee(user_id)
