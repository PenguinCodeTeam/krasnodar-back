from datetime import timedelta

from fastapi import APIRouter

from internal.core.types import PriorityEnum


TASKS_ROUTER = APIRouter(prefix='/tasks', tags=['Tasks'])


@TASKS_ROUTER.get('/{task_id}')
async def get_task_handler(task_id: int):
    return {
        'name': 'Выезд на точку для стимулирования выдач',
        'priority': PriorityEnum.HIGH,
        'time': str(timedelta(hours=5)),
        'point': {'latitude': 3.0, 'longitude': 12.523},
    }
