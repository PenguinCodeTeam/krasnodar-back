import asyncio
from datetime import date, timedelta

from internal.repositories.db import PointRepository, TaskRepository
from internal.tasks.worker import celery


async def async_generate_tasks():
    task_repository = TaskRepository()
    point_repository = PointRepository()
    destinations = await point_repository.get_destinations()

    delivery_cards = await task_repository.get_task_type(name='Доставка карт и материалов')
    educate_agent = await task_repository.get_task_type(name='Обучение агента')
    stimulating_issuances = await task_repository.get_task_type(name='Выезд на точку для стимулирования выдач')

    task_type_ids_and_statements = [
        {
            'task_type_id': delivery_cards.id,
            'statement': lambda destination: destination.created_at >= date.today() - timedelta(days=1) or not destination.is_delivered,
        },
        {'task_type_id': educate_agent.id, 'statement': lambda destination: destination.completed_requests > 0 and destination.percent_completed_requests < 50},
        {
            'task_type_id': stimulating_issuances.id,
            'statement': lambda destination: destination.days_after_delivery > 7
            and destination.percent_completed_requests < 100
            or destination.days_after_delivery > 14,
        },
    ]

    for destination in destinations:
        for task_type in task_type_ids_and_statements:
            if task_type['statement'](destination):
                if await task_repository.get_task(task_type_id=task_type['task_type_id'], point_id=destination.point_id) is None:
                    await task_repository.add_task(task_type_id=task_type['task_type_id'], point_id=destination.point_id)


@celery.task(name='generate_tasks')
def generate_tasks():
    return asyncio.get_event_loop().run_until_complete(async_generate_tasks())
