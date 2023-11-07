from uuid import UUID, uuid4

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.tasks import GetTasksRequest, UpdateTaskRequest
from internal.api.v1.schemas.response.tasks import GetTaskResponse, GetTasksResponse
from internal.core.types import PriorityEnum


TASKS_ROUTER = APIRouter(prefix='/tasks', tags=['Tasks'])


@TASKS_ROUTER.get('/{task_id}', tags=['Not working'])
async def get_task_handler(task_id: UUID) -> GetTaskResponse:
    """Получение задачи по id"""
    return GetTaskResponse(
        id=uuid4(),
        name='Выезд на точку для стимулирования выдач',
        priority=PriorityEnum.HIGH,
        time=90,
        point={'latitude': 3.0, 'longitude': 12.523},
    )


@TASKS_ROUTER.put('/{task_id}', tags=['Not working'])
async def update_task_handler(task_id: UUID, request_data: UpdateTaskRequest) -> None:
    """Изменение задачи"""
    pass


@TASKS_ROUTER.get('/', tags=['Not working'])
async def get_all_tasks_handler(request_data: GetTasksRequest = Depends()) -> GetTasksResponse:
    """Получение всех задач с фильтрацией по дате и пользователю"""
    pass
