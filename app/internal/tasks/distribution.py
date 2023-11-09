import asyncio
from collections import defaultdict
from uuid import UUID

from internal.core.types import PriorityEnum, TaskStatusEnum, WorkerGradeEnum
from internal.repositories.db import PointRepository, TaskRepository, UserRepository
from internal.repositories.db.models import Task
from internal.tasks.worker import celery


MAX_WORKING_MINUTES = 8 * 60


async def generate_tasks_for_graph() -> dict:
    task_repository = TaskRepository()

    senior_high_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.SENIOR, priority=PriorityEnum.HIGH, status=TaskStatusEnum.OPEN)
    senior_medium_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.SENIOR, priority=PriorityEnum.MEDIUM, status=TaskStatusEnum.OPEN)
    senior_low_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.SENIOR, priority=PriorityEnum.LOW, status=TaskStatusEnum.OPEN)

    middle_high_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.MIDDLE, priority=PriorityEnum.HIGH, status=TaskStatusEnum.OPEN)
    middle_medium_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.MIDDLE, priority=PriorityEnum.MEDIUM, status=TaskStatusEnum.OPEN)
    middle_low_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.MIDDLE, priority=PriorityEnum.LOW, status=TaskStatusEnum.OPEN)

    junior_high_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.JUNIOR, priority=PriorityEnum.HIGH, status=TaskStatusEnum.OPEN)
    junior_medium_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.JUNIOR, priority=PriorityEnum.MEDIUM, status=TaskStatusEnum.OPEN)
    junior_low_priority_tasks = await task_repository.get_tasks(grade=WorkerGradeEnum.JUNIOR, priority=PriorityEnum.LOW, status=TaskStatusEnum.OPEN)

    return {
        WorkerGradeEnum.SENIOR: {
            PriorityEnum.HIGH: senior_high_priority_tasks,
            PriorityEnum.MEDIUM: senior_medium_priority_tasks,
            PriorityEnum.LOW: senior_low_priority_tasks,
        },
        WorkerGradeEnum.MIDDLE: {
            PriorityEnum.HIGH: middle_high_priority_tasks,
            PriorityEnum.MEDIUM: middle_medium_priority_tasks,
            PriorityEnum.LOW: middle_low_priority_tasks,
        },
        WorkerGradeEnum.JUNIOR: {
            PriorityEnum.HIGH: junior_high_priority_tasks,
            PriorityEnum.MEDIUM: junior_medium_priority_tasks,
            PriorityEnum.LOW: junior_low_priority_tasks,
        },
    }


async def generate_graph() -> dict:
    point_repository = PointRepository()
    task_repository = TaskRepository()

    graph = defaultdict(dict)
    all_tasks = await task_repository.get_tasks()
    workplaces = await point_repository.get_workplaces()

    for workplace in workplaces:
        for task in all_tasks:
            if task.point_id in graph[workplace.point.id]:
                continue
            graph[workplace.point.id][task.point_id] = await point_repository.get_points_duration(workplace.point.id, task.point_id)

    for from_task in all_tasks:
        for to_task in all_tasks:
            if task.point_id in graph[workplace.point.id] or from_task.point_id == to_task.point_id:
                continue
            graph[from_task.point_id][to_task.point_id] = await point_repository.get_points_duration(from_task.point_id, to_task.point_id)

    return graph


def get_best_route(
    graph: dict,
    used_points: set,
    grouped_tasks: dict,
    current_point: UUID,
    route: list[Task] = [],
    used_hours: int = 0,
) -> list:
    for _, tasks in grouped_tasks:
        best_route = route
        for task in tasks:
            if task.point_id in used_points or task in [data['task'] for data in route]:
                continue
            if used_hours + task.task_type.duration + graph[current_point][task.point_id] <= MAX_WORKING_MINUTES:
                route.append({'task': task, 'duration_to_task': graph[current_point][task.point_id]})
                new_route: list = get_best_route(
                    graph=graph,
                    used_hours=used_hours + task.task_type.duration + graph[current_point][task.point_id],
                    used_points=used_points,
                    grouped_tasks=grouped_tasks,
                    route=route,
                    current_point=task.point_id,
                )
                route.pop(-1)
                if len(new_route) > best_route:
                    best_route = new_route.copy()
                    del new_route
        route = best_route.copy()
        del best_route

    return route


async def save_tasks_by_workers(distributed_tasks_by_workers: dict):
    task_repository = TaskRepository()
    for user_id, tasks in distributed_tasks_by_workers.items():
        await task_repository.add_work_schedule(user_id=user_id, tasks=tasks)


async def async_tasks_distribution():
    point_repository = UserRepository()
    grouped_tasks = await generate_tasks_for_graph()
    graph = await generate_graph()

    distributed_tasks_by_workers = {}
    workers = await point_repository.get_workers(is_active=True)
    workers_by_grade = defaultdict(list)
    for worker in workers:
        workers_by_grade[worker.grade].append(worker)
    used_points = set()
    for grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE, WorkerGradeEnum.JUNIOR]:
        for worker in workers_by_grade[grade]:
            distributed_tasks_by_workers[worker.id] = get_best_route(
                graph=graph,
                used_points=used_points,
                list_of_available_tasks=grouped_tasks[grade],
                current_point=worker.workplace_id,
            )
            for task in distributed_tasks_by_workers[worker.id]:
                used_points.add(task.point_id)

    await save_tasks_by_workers(distributed_tasks_by_workers)


@celery.task(name='tasks_distribution')
def tasks_distribution():
    asyncio.get_event_loop().run_until_complete(async_tasks_distribution())
