from uuid import UUID

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.tasks import GetAppointedTasksRequest, GetTasksRequest, UpdateAppointedTaskRequest
from internal.api.v1.schemas.response.tasks import (
    GetAppointedTaskResponse,
    GetAppointedTasksResponse,
    GetTaskResponse,
    GetTasksResponse,
    GetTaskTypeResponse,
    GetTaskTypesResponse,
)
from internal.core.dependencies.authorization import EmployeeAuthorize
from internal.services.task import TaskService


TASKS_ROUTER = APIRouter(prefix='/task', tags=['Tasks'], dependencies=[Depends(EmployeeAuthorize())])


@TASKS_ROUTER.get('/type/{task_type_id}')
async def get_task_type_handler(task_type_id: int, service: TaskService = Depends()) -> GetTaskTypeResponse:
    """Получение информации о типе задачи по её id"""
    data = await service.get_task_type(task_type_id=task_type_id)
    return GetTaskTypeResponse.model_validate(data)


@TASKS_ROUTER.get('/type')
async def get_task_types_handler(service: TaskService = Depends()) -> GetTaskTypesResponse:
    """Получение всех типов задач"""
    data = await service.get_task_types()
    return GetTaskTypesResponse(task_types=data)


@TASKS_ROUTER.get('/appointed/{task_id}')
async def get_appointed_task_handler(task_id: UUID, service: TaskService = Depends()) -> GetAppointedTaskResponse:
    """Получение назначенной задачи по id"""
    data = await service.get_appointed_task(task_id)
    return GetAppointedTaskResponse.model_validate(data)


# TODO: Authorization only for owner of task
@TASKS_ROUTER.put('/appointed/{task_id}')
async def update_appointed_task_handler(task_id: UUID, request_data: UpdateAppointedTaskRequest, service: TaskService = Depends()) -> GetAppointedTaskResponse:
    """Изменение назначенной задачи"""
    data = await service.update_appointed_task(task_id, request_data.status, request_data.message)
    return GetAppointedTaskResponse.model_validate(data)


# TODO: Authorization only for owner of tasks
@TASKS_ROUTER.get('/appointed')
async def get_appointed_tasks_handler(request_data: GetAppointedTasksRequest = Depends(), service: TaskService = Depends()) -> GetAppointedTasksResponse:
    """Получение всех задач с фильтрацией по дате. Может использоваться для получения всех задач пользователя"""
    data = await service.get_appointed_tasks(**request_data.model_dump(exclude_none=True))
    return GetAppointedTasksResponse(tasks=data)


@TASKS_ROUTER.get('')
async def get_tasks_handler(request_data: GetTasksRequest = Depends(), service: TaskService = Depends()) -> GetTasksResponse:
    """Получение задач по фильтрам"""
    data = await service.get_tasks(**request_data.model_dump(exclude_none=True))
    return GetTasksResponse(tasks=data)


@TASKS_ROUTER.get('/{task_id}')
async def get_task_handler(task_id: UUID, service: TaskService = Depends()) -> GetTaskResponse:
    """Получение задачи по её id"""
    data = await service.get_task(task_id)
    return GetTaskResponse.model_validate(data)
