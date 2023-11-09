from collections import defaultdict
from uuid import UUID

from fastapi.exceptions import HTTPException

from internal.core.types import CeleryTaskStatusEnum
from internal.repositories.db.celery import CeleryTaskRepository
from internal.repositories.db.tasks import TaskRepository
from internal.repositories.db.users import UserRepository
from internal.tasks import get_task_by_id, tasks_distribution


class DistributionService:
    def __init__(self):
        self.celery_task_id_repository = CeleryTaskRepository()
        self.task_repository = TaskRepository()
        self.user_repository = UserRepository()

    async def start_distribution(self):
        task = await self.celery_task_id_repository.get_task(task_name='tasks_distribution')
        if task is not None:
            task = get_task_by_id(str(task.id))
            if not task.ready():
                return HTTPException(status_code=423, detail='Locked.')

        task = tasks_distribution.delay()
        await self.celery_task_id_repository.update_task(task_id=UUID(task.id), task_name='tasks_distribution')
        response = {'status': get_status(task.status), 'result': None}
        if task.successful():
            response['result'] = await get_result(self.task_repository, self.user_repository)
        return response

    async def get_distribution_result(self):
        task = await self.celery_task_id_repository.get_task(task_name='tasks_distribution')
        if task is None:
            raise HTTPException(status_code=404, detail='Not found.')
        task = get_task_by_id(str(task.id))
        response = {'status': get_status(task.status), 'result': None}
        if task.successful():
            response['result'] = await get_result(self.task_repository, self.user_repository)
        return response


async def get_result(task_repository: TaskRepository, user_repository: UserRepository):
    work_schedule = await task_repository.get_work_schedule()
    tasks_by_worker = defaultdict(list)
    for work_schedule_task in work_schedule:
        tasks_by_worker[work_schedule_task.user_id].append(
            {
                'full_address': 'г. ' + work_schedule_task.task.point.city + ', ' + work_schedule_task.task.point.address,
                'task_number': work_schedule_task.task_number,
                'date': work_schedule_task.date,
                'expected_start_at': work_schedule_task.expected_start_at,
                'expected_finish_at': work_schedule_task.expected_finish_at,
                'started_at': work_schedule_task.started_at,
                'finished_at': work_schedule_task.finished_at,
            }
        )
    workers = await user_repository.get_workers(is_active=True)
    result = {'workers_distribution': []}
    for worker in workers:
        result['workers_distribution'].append(
            {
                'worker': {
                    'full_address': 'г. ' + worker.workplace.point.city + ', ' + worker.workplace.point.address,
                    'name': worker.user.name,
                    'surname': worker.user.surname,
                    'login': worker.user.login,
                    'patronymic': worker.user.patronymic,
                    'grade': worker.grade,
                },
                'tasks': tasks_by_worker[worker.user_id],
            }
        )
    return result


def get_status(status: str):
    match status:
        case 'SUCCESS':
            return CeleryTaskStatusEnum.OK
        case 'FAILURE':
            return CeleryTaskStatusEnum.ERROR
        case _:
            return CeleryTaskStatusEnum.IN_PROGRESS
