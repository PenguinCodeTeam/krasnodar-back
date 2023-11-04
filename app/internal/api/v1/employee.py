from datetime import timedelta
from uuid import uuid4

from fastapi import APIRouter, Body

from internal.api.v1.schemas.request.employee import CreateEmployeeUserRequest, FinishTaskRequest, UpdateUserRequest
from internal.api.v1.schemas.response.employee import GetEmployeeInfo, GetEmployeeTasksResponse, GetEmployeeUserResponse
from internal.core.types import PriorityEnum


EMPLOYEE_ROUTER = APIRouter(prefix='/employee')


@EMPLOYEE_ROUTER.get('/tasks', tags=['Employee'])
async def get_employee_tasks_handler(user_id: int):
    return GetEmployeeTasksResponse(
        tasks=[
            {
                'id': uuid4(),
                'name': 'Выезд на точку для стимулирования выдач',
                'priority': PriorityEnum.HIGH,
                'time': timedelta(hours=5),
                'point': {'latitude': 3.0, 'longitude': 12.523},
            }
        ]
    )


@EMPLOYEE_ROUTER.get('/', tags=['Employee'])
async def get_employee_info_handler():
    return GetEmployeeInfo(name='Дерягин', surname='Никита', patronymic='Владимирович', address='Краснодар, Красная, д. 139', grade='Синьор')


@EMPLOYEE_ROUTER.post('/finish_task/{task_id}', tags=['Employee'])
async def finish_task_handler(task_id: int, request_data: FinishTaskRequest):
    return None


# ONLY FOR MANAGER
@EMPLOYEE_ROUTER.get('/{user_id}', tags=['Manager'])
async def get_employee_handler(user_id: int):
    return GetEmployeeUserResponse(name='Дерягин', surname='Никита', patronymic='Владимирович', address='Краснодар, Красная, д. 139', grade='Синьор')


@EMPLOYEE_ROUTER.post('/', tags=['Manager'])
async def create_employee_handler(user_id: int, request_data: CreateEmployeeUserRequest = Body()):
    return None


@EMPLOYEE_ROUTER.patch('/{user_id}', tags=['Manager'])
async def update_employee_handler(user_id: int, request_data: UpdateUserRequest = Body()):
    return None
