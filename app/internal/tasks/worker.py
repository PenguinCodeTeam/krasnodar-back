from celery import Celery
from celery.result import AsyncResult
from config import REDIS_HOST, REDIS_PORT


celery = Celery(__name__)
celery.conf.broker_url = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
celery.conf.result_backend = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'


def get_last_task_id_by_name(task_name: str):
    result_backend = celery.backend
    task_ids = result_backend.get_task_meta_for(task_name)

    if task_ids:
        last_task_id = task_ids[-1].task_id
        return last_task_id
    else:
        return None


def get_status_by_task_id(task_id: str):
    result = AsyncResult(task_id, app=celery)
    return result.status
