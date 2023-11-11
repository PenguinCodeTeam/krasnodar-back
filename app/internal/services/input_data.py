import datetime
from uuid import UUID

from fastapi.exceptions import HTTPException

from internal.core.types import CeleryTaskStatusEnum
from internal.repositories.db.celery import CeleryTaskRepository
from internal.tasks import get_task_by_id, update_input_data


class InputDataService:
    def __init__(self):
        self.celery_task_id_repository = CeleryTaskRepository()

    async def set_input_data(self, destinations: dict, city: str):
        task = await self.celery_task_id_repository.get_task(task_name='update_input_data', date=datetime.date.today())
        if task is not None:
            task = get_task_by_id(str(task.id))
            if not task.ready():
                raise HTTPException(status_code=423, detail='Locked.')

        task = update_input_data.delay(destinations, city, for_date=datetime.date.today())
        await self.celery_task_id_repository.update_task(task_id=UUID(task.id), task_name='update_input_data')
        response = {'status': get_status(task.status), 'result': None}
        if task.successful():
            response['result'] = await task.result
        return response

    async def get_input_data(self, date: datetime.date):
        task = await self.celery_task_id_repository.get_task(task_name='update_input_data', date=date)
        if task is None:
            raise HTTPException(status_code=404, detail='Not found.')
        task = get_task_by_id(str(task.id))
        response = {'status': get_status(task.status), 'result': None}
        if task.successful():
            response['result'] = task.result
        return response


def get_status(status: str):
    match status:
        case 'SUCCESS':
            return CeleryTaskStatusEnum.OK
        case 'FAILURE':
            return CeleryTaskStatusEnum.ERROR
        case _:
            return CeleryTaskStatusEnum.IN_PROGRESS
