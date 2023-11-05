from uuid import UUID

from fastapi import APIRouter, Body

from internal.api.v1.schemas.request.employee import CreateEmployeeUserRequest, UpdateUserRequest
from internal.api.v1.schemas.response.employee import GetAllEmployeesResponse, GetEmployeeUserResponse


EMPLOYEE_ROUTER = APIRouter(prefix='/employee', tags=['Employee'])


@EMPLOYEE_ROUTER.get('/')
async def get_all_employees_handler() -> GetAllEmployeesResponse:
    """Получение всех сотрудников. Для менеджера"""
    pass


@EMPLOYEE_ROUTER.post('/')
async def create_employee_handler(request_data: CreateEmployeeUserRequest = Body()):
    """Создание профиля работника. Для менеджера"""
    return None


@EMPLOYEE_ROUTER.get('/{user_id}')
async def get_employee_handler(user_id: UUID) -> GetEmployeeUserResponse:
    """Получение инмформации о работнике по id. Для менеджера"""
    return GetEmployeeUserResponse(name='Дерягин', surname='Никита', patronymic='Владимирович', address='Краснодар, Красная, д. 139', grade='Синьор')


@EMPLOYEE_ROUTER.patch('/{user_id}')
async def update_employee_handler(user_id: UUID, request_data: UpdateUserRequest = Body()):
    """Обновление профиля работнике. Для менеджера"""
    return None
