from uuid import UUID

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.tasks import GetTasksRequest, UpdateTaskRequest
from internal.api.v1.schemas.response.tasks import GetAppointedAppointedTaskResponse, GetAppointedTasksResponse
from internal.core.dependencies.authorization import EmployeeAuthorize
from internal.services.task import TaskService


TASKS_ROUTER = APIRouter(prefix='/tasks', tags=['Tasks'], dependencies=[Depends(EmployeeAuthorize())])


# TODO: Authorization only for owner of task
@TASKS_ROUTER.get('/appointed/{task_id}')
async def get_task_handler(task_id: UUID, service: TaskService = Depends()):
    """Получение задачи по id"""
    data = await service.get_appointed_task(task_id)
    return data


# TODO: Authorization only for owner of tasks
@TASKS_ROUTER.put('/appointed/{task_id}')
async def update_task_handler(task_id: UUID, request_data: UpdateTaskRequest, service: TaskService = Depends()) -> GetAppointedAppointedTaskResponse:
    """Изменение задачи"""
    data = await service.update_appointed_task(task_id, request_data.status, request_data.message)
    return GetAppointedAppointedTaskResponse.model_validate(data)


@TASKS_ROUTER.get('/appointed/')
async def get_tasks_handler(request_data: GetTasksRequest = Depends(), service: TaskService = Depends()) -> GetAppointedTasksResponse:
    """Получение всех задач с фильтрацией по дате и пользователю"""
    data = await service.get_appointed_tasks(**request_data.model_dump(exclude_none=True))
    return GetAppointedTasksResponse(tasks=data)
