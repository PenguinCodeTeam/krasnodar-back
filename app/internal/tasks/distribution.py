import asyncio
from collections import defaultdict
from datetime import date, timedelta

from internal.core.types import WorkerGradeEnum
from internal.repositories.db import PointRepository, TaskRepository, UserRepository
from internal.tasks.models import GradeTasks, GraphElement, Point, Task
from internal.tasks.worker import celery


MAX_WORKING_MINUTES = 8 * 60


async def generate_tasks() -> GradeTasks:
    point_repository = PointRepository()
    task_repository = TaskRepository()
    senior_task = await task_repository.get_task(name='Выезд на точку для стимулирования выдач')
    middle_task = await task_repository.get_task(name='Обучение агента')
    junior_task = await task_repository.get_task(name='Доставка карт и материалов')
    senior_points_statement_1 = await point_repository.get_destinations(le_days_after_delivery=8, lt_percent_completed_requests=100, point_completed=False)
    senior_points_statement_2 = await point_repository.get_destinations(le_days_after_delivery=15, point_completed=False)
    senior_points = list(set().union(senior_points_statement_1, senior_points_statement_2))

    middle_points = await point_repository.get_destinations(lt_percent_completed_requests=50, point_completed=False)

    junior_points_statement_1 = await point_repository.get_destinations(ge_created_at=date.today() - timedelta(days=1), point_completed=False)
    junior_points_statement_2 = await point_repository.get_destinations(is_delivered=False, point_completed=False)
    junior_points = list(set().union(junior_points_statement_1, junior_points_statement_2))

    senior_tasks = [
        Task(
            point=Point.model_validate(point.point),
            task_id=senior_task.id,
            name=senior_task.name,
            priority=senior_task.priority,
            duration_work=senior_task.duration,
        )
        for point in senior_points
    ]
    middle_tasks = [
        Task(
            point=Point.model_validate(point.point),
            task_id=middle_task.id,
            name=middle_task.name,
            priority=middle_task.priority,
            duration_work=middle_task.duration,
        )
        for point in middle_points
    ]
    junior_tasks = [
        Task(
            point=Point.model_validate(point.point),
            task_id=junior_task.id,
            name=junior_task.name,
            priority=junior_task.priority,
            duration_work=junior_task.duration,
        )
        for point in junior_points
    ]

    return GradeTasks(
        junior_tasks=junior_tasks,
        middle_tasks=middle_tasks,
        senior_tasks=senior_tasks,
    )


async def generate_graph(tasks: GradeTasks) -> dict:
    point_repository = PointRepository()
    graph = defaultdict(dict)
    all_tasks = tasks.senior + tasks.middle + tasks.junior
    workplaces = await point_repository.get_workplaces()

    for workplace in workplaces:
        for task in all_tasks:
            graph[workplace.point.id][task.point.id] = GraphElement(
                duration=await point_repository.get_points_duration(workplace.point.id, task.point.id),
                task=task,
            )

    for from_task in all_tasks:
        for to_task in all_tasks:
            if from_task is not to_task:
                graph[from_task.point.id][to_task.point.id] = GraphElement(
                    duration=await point_repository.get_points_duration(from_task.point.id, to_task.point.id),
                    task=to_task,
                )

    return graph


def get_available_tasks(grade: WorkerGradeEnum, tasks: GradeTasks) -> GradeTasks:
    list_of_available_tasks = []
    if grade == WorkerGradeEnum.SENIOR:
        list_of_available_tasks.append(tasks.senior)
    if grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE]:
        list_of_available_tasks.append(tasks.middle)
    if grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE, WorkerGradeEnum.JUNIOR]:
        list_of_available_tasks.append(tasks.junior)
    return list_of_available_tasks


def get_best_route(
    graph: dict,
    used_tasks: set,
    list_of_available_tasks: list[list[Task]],
    current_point: Point,
    route: list[Task] = [],
    used_hours: int = 0,
) -> list:
    for tasks in list_of_available_tasks:
        best_route = route
        for task in tasks:
            if task in used_tasks or task in route:
                continue
            if used_hours + task.duration_work + graph[current_point][task.point] <= MAX_WORKING_MINUTES:
                route.append(task)
                new_route: list = get_best_route(
                    graph=graph,
                    used_hours=used_hours + task.duration_work + graph[current_point][task.point],
                    used_tasks=used_tasks,
                    list_of_grade_points=list_of_available_tasks,
                    route=route,
                    current_point=current_point,
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
        await task_repository.add_schedule_tasks(user_id=user_id, tasks=tasks)


@celery.task(name='tasks_distribution')
def tasks_distribution():
    point_repository = UserRepository()
    tasks_by_grade = asyncio.run(generate_tasks())
    graph = asyncio.run(generate_graph())
    tasks_for_grade = {
        grade: get_available_tasks(grade=grade, tasks=tasks_by_grade) for grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE, WorkerGradeEnum.JUNIOR]
    }

    distributed_tasks_by_workers = {}
    workers = asyncio.run(point_repository.get_workers())
    workers_by_grade = defaultdict(list)
    for worker in workers:
        workers_by_grade[worker.grade].append(worker)
    used_tasks = set()
    for grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE, WorkerGradeEnum.JUNIOR]:
        for worker in workers_by_grade[grade]:
            distributed_tasks_by_workers[worker.id] = get_best_route(
                graph=graph,
                used_tasks=used_tasks,
                list_of_available_tasks=tasks_for_grade[grade],
                current_point=worker.point,
            )
            used_tasks.union(distributed_tasks_by_workers[worker.id])

    asyncio.run(save_tasks_by_workers(distributed_tasks_by_workers))
