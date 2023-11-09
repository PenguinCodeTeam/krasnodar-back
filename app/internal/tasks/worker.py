from celery import Celery
from celery.result import AsyncResult
from config import REDIS_DB, REDIS_HOST, REDIS_PORT


REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

celery = Celery(__name__)
celery.conf.broker_url = REDIS_URL
celery.conf.result_backend = REDIS_URL


def get_task_by_id(task_id: str):
    return AsyncResult(task_id, app=celery)
