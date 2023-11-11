import asyncio
from collections import defaultdict
from datetime import date
from uuid import UUID

from internal.core.types import PriorityEnum, TaskStatusEnum, WorkerGradeEnum
from internal.repositories.db import PointRepository, TaskRepository, UserRepository
from internal.repositories.db.celery import CeleryTaskRepository
from internal.repositories.db.models import Task
from internal.tasks.worker import celery, get_task_by_id


MAX_WORKING_MINUTES = 8 * 60


async def generate_tasks_for_graph() -> dict:
    task_repository = TaskRepository()

    grouped_tasks = {
        WorkerGradeEnum.SENIOR: defaultdict(dict),
        WorkerGradeEnum.MIDDLE: defaultdict(dict),
        WorkerGradeEnum.JUNIOR: defaultdict(dict),
    }
    tasks = await task_repository.get_tasks(status=TaskStatusEnum.OPEN, le_date=date.today())
    for task in tasks:
        for task_grade in task.task_type.task_grades:
            if task.task_type.priority not in grouped_tasks[task_grade.grade][task.active_from]:
                grouped_tasks[task_grade.grade][task.active_from][task.task_type.priority] = []
            grouped_tasks[task_grade.grade][task.active_from][task.task_type.priority].append(task)

    return grouped_tasks


async def generate_graph() -> dict:
    point_repository = PointRepository()
    task_repository = TaskRepository()

    graph = defaultdict(dict)
    all_tasks = await task_repository.get_tasks(le_date=date.today(), status=TaskStatusEnum.OPEN)

    workplaces = await point_repository.get_workplaces()

    for workplace in workplaces:
        for task in all_tasks:
            graph[workplace.point_id][task.point_id] = await point_repository.get_points_duration(workplace.point.id, task.point_id)

    for from_task in all_tasks:
        for to_task in all_tasks:
            if from_task.point_id == to_task.point_id:
                continue
            graph[from_task.point_id][to_task.point_id] = await point_repository.get_points_duration(from_task.point_id, to_task.point_id)

    return graph


def bruteforce_route(
    graph: dict,
    used_points: set,
    tasks: list[Task],
    current_point: UUID,
    route: list[Task] = [],
    used_hours: int = 0,
):
    best_route = route.copy()
    best_used_hours = used_hours
    for task in tasks:
        if task.point_id in used_points or task.point_id in [data['task'].point_id for data in route]:
            continue
        if used_hours + task.task_type.duration + graph[current_point][task.point_id].duration <= MAX_WORKING_MINUTES:
            new_route, new_used_hours = bruteforce_route(
                graph=graph,
                used_hours=used_hours + task.task_type.duration + graph[current_point][task.point_id].duration,
                used_points=used_points,
                tasks=tasks,
                route=route.copy() + [{'task': task, 'duration_to_task': graph[current_point][task.point_id].duration}],
                current_point=task.point_id,
            )
            if len(new_route) > len(best_route) or len(new_route) == len(best_route) and new_used_hours < best_used_hours:
                best_used_hours = new_used_hours
                best_route = new_route.copy()
                del new_route
    return best_route, best_used_hours


def get_best_route(
    graph: dict,
    used_points: set,
    grouped_tasks: dict,
    current_point: UUID,
) -> list:
    used_hours = 0
    route = []
    for active_from in sorted(grouped_tasks.keys()):
        updated_grouped_tasks_with_priority = {}
        if PriorityEnum.HIGH in grouped_tasks[active_from]:
            updated_grouped_tasks_with_priority[PriorityEnum.HIGH] = grouped_tasks[active_from][PriorityEnum.HIGH]
        if PriorityEnum.MEDIUM in grouped_tasks[active_from]:
            updated_grouped_tasks_with_priority[PriorityEnum.MEDIUM] = grouped_tasks[active_from][PriorityEnum.MEDIUM]
        if PriorityEnum.LOW in grouped_tasks[active_from]:
            updated_grouped_tasks_with_priority[PriorityEnum.LOW] = grouped_tasks[active_from][PriorityEnum.LOW]
        for _, tasks in updated_grouped_tasks_with_priority.items():
            route, used_hours = bruteforce_route(
                graph=graph,
                used_points=used_points,
                tasks=tasks,
                current_point=current_point,
                route=route.copy(),
                used_hours=used_hours,
            )

    return route, used_hours


async def save_tasks_by_workers(task_repository: TaskRepository, distributed_tasks_by_workers: dict):
    await task_repository.delete_work_schedule()

    for user_id, route in distributed_tasks_by_workers.items():
        await task_repository.add_work_schedule(user_id=user_id, route=route)


async def async_tasks_distribution():
    celery_task_repository = CeleryTaskRepository()
    while True:
        task = await celery_task_repository.get_task(task_name='update_input_data', date=date.today())
        if task is not None:
            task = get_task_by_id(str(task.id))
            if task.ready():
                break
        else:
            break

    while True:
        task = await celery_task_repository.get_task(task_name='load_durations_for_workplace', date=date.today())
        if task is not None:
            task = get_task_by_id(str(task.id))
            if task.ready():
                break
        else:
            break

    point_repository = UserRepository()
    task_repository = TaskRepository()

    work_schedule = await task_repository.get_work_schedule(date=date.today())
    unique_task_ids = set()
    for work_schedule_task in work_schedule:
        if work_schedule_task.task_id not in unique_task_ids:
            await task_repository.update_task(work_schedule_task.task, status=TaskStatusEnum.OPEN)
            unique_task_ids.add(work_schedule_task.task_id)

    grouped_tasks = await generate_tasks_for_graph()
    graph = await generate_graph()

    distributed_tasks_by_workers = {}
    workers = await point_repository.get_workers()
    workers_by_grade = defaultdict(list)
    for worker in workers:
        workers_by_grade[worker.grade].append(worker)
    used_points = set()
    for grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE, WorkerGradeEnum.JUNIOR]:
        for worker in workers_by_grade[grade]:
            distributed_tasks_by_workers[worker.user_id], _ = get_best_route(
                graph=graph,
                used_points=used_points,
                grouped_tasks=grouped_tasks[grade],
                current_point=worker.workplace_id,
            )
            for task in distributed_tasks_by_workers[worker.user_id]:
                used_points.add(task['task'].point_id)

    await save_tasks_by_workers(task_repository, distributed_tasks_by_workers)


@celery.task(name='tasks_distribution')
def tasks_distribution():
    asyncio.get_event_loop().run_until_complete(async_tasks_distribution())
