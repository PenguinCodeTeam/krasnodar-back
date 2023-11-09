from uuid import UUID

from fastapi.exceptions import HTTPException

from internal.core.types import CeleryTaskStatus
from internal.repositories.db.celery import CeleryTaskIdRepository
from internal.tasks import get_task_by_id, update_input_data


class InputDataService:
    def __init__(self):
        self.celery_task_id_repository = CeleryTaskIdRepository()

    async def set_input_data(self, destinations: dict, task_types: dict, workers: dict):
        task = await self.celery_task_id_repository.get_task(task_name='update_input_data')
        if task is not None:
            task = get_task_by_id(str(task.id))
            if not task.ready():
                return HTTPException(status_code=423, detail='Locked.')

        task = update_input_data.delay(destinations, task_types, workers)
        await self.celery_task_id_repository.update_task(task_id=UUID(task.id), task_name='update_input_data')
        response = {'status': get_status(task.status), 'result': None}
        if task.successful():
            response['result'] = await task.result
        return response

    async def get_input_data(self):
        task = await self.celery_task_id_repository.get_task(task_name='update_input_data')
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
            return CeleryTaskStatus.OK
        case 'FAILURE':
            return CeleryTaskStatus.ERROR
        case _:
            return CeleryTaskStatus.IN_PROGRESS
