import datetime
import zoneinfo
from typing import Type
from uuid import UUID

from fastapi.exceptions import HTTPException

from internal.core.types import Empty, PriorityEnum, TaskStatusEnum, WorkerGradeEnum
from internal.repositories.db.models import Point, Task, TaskType, WorkSchedule
from internal.repositories.db.tasks import TaskRepository


class TaskService:
    def __init__(self):
        self.repository = TaskRepository()

    async def get_appointed_tasks(
        self,
        date: datetime.date,
        user_id: UUID | Type[Empty] = Empty,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
        priority: PriorityEnum | Type[Empty] = Empty,
        status: TaskStatusEnum | Type[Empty] = Empty,
    ) -> list[dict]:
        tasks = await self.repository.get_work_schedule(date=date, user_id=user_id, grade=grade, priority=priority, status=status)
        return [form_appointed_task_response(task) for task in tasks]

    async def get_appointed_task(self, task_id: UUID) -> dict:
        tasks = await self.repository.get_work_schedule(task_id)
        if not tasks:
            raise HTTPException(status_code=404, detail='Task not found')
        return form_appointed_task_response(tasks[0])

    async def update_appointed_task(self, task_id: UUID, status: TaskStatusEnum, message: str) -> dict:
        tasks = await self.repository.get_work_schedule(task_id)
        if not tasks:
            raise HTTPException(status_code=404, detail='Task not found')
        schedule_task = tasks[0]

        schedule_task.task = await self.repository.update_task(schedule_task.task, status, message)
        return form_appointed_task_response(schedule_task)

    async def get_task(self, task_id: UUID) -> dict:
        task = await self.repository.get_task(task_id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')

        return form_task_response(task)

    async def get_tasks(
        self,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
        priority: PriorityEnum | Type[Empty] = Empty,
        status: TaskStatusEnum | Type[Empty] = Empty,
        task_type_id: UUID | Type[Empty] = Empty,
    ):
        tasks = await self.repository.get_tasks(grade=grade, priority=priority, status=status, task_type_id=task_type_id)

        return [form_task_response(task) for task in tasks]

    async def get_task_type(self, task_type_id: int):
        task_type = await self.repository.get_task_type(task_type_id=task_type_id)
        if not task_type:
            raise HTTPException(status_code=404, detail='Task type not found')
        return form_task_type_response(task_type)

    async def get_task_types(self):
        task_types = await self.repository.get_task_types()
        return [form_task_type_response(task_type) for task_type in task_types]


def form_task_type_response(task_type: TaskType):
    return {'id': task_type.id, 'name': task_type.name, 'priority': task_type.priority, 'duration': task_type.duration}


def form_task_response(task: Task) -> dict:
    task_type: TaskType = task.task_type
    task_point: Point = task.point

    return {
        'id': task.id,
        'status': task.status,
        'name': task_type.name,
        'task_type_id': task_type.id,
        'message': task.message if task.message else '',
        'priority': task_type.priority,
        'time': task_type.duration,
        'point': {
            'id': task_point.id,
            'full_address': f'г. {task_point.city}, {task_point.address}',
        },
        'created_date': task.active_from,
    }


def form_appointed_task_response(schedule_task: WorkSchedule) -> dict:
    task: Task = schedule_task.task
    task_type: TaskType = task.task_type
    task_point: Point = task.point

    return {
        'id': task.id,
        'status': task.status,
        'name': task_type.name,
        'task_type_id': task_type.id,
        'message': task.message if task.message else '',
        'priority': task_type.priority,
        'time': task_type.duration,
        'point': {
            'id': task_point.id,
            'full_address': f'г. {task_point.city}, {task_point.address}',
        },
        'created_date': task.active_from,
        'date': schedule_task.date,
        'task_number': schedule_task.task_number,
        'started_at': strtime_from_timestamp(schedule_task.expected_start_at),
        'finished_at': strtime_from_timestamp(schedule_task.expected_finish_at),
    }


def strtime_from_timestamp(timestamp: int):
    dt = datetime.datetime.fromtimestamp(timestamp, tz=zoneinfo.ZoneInfo('Europe/Moscow'))
    return dt.time().strftime('%H:%M')
