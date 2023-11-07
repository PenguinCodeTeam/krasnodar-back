from collections import defaultdict
from datetime import date, timedelta

from internal.core.types import PriorityEnum, WorkerGradeEnum
from internal.repositories.db import PointRepository, UserRepository
from internal.tasks.models import GradeTasks, GraphElement, Point, Task
from internal.tasks.worker import celery


MAX_WORKING_MINUTES = 8 * 60
SENIOR_TASKS_DURATION_MINUTES = 4 * 60
MIDDLE_TASKS_DURATION_MINUTES = 2 * 60
JUNIOR_TASKS_DURATION_MINUTES = 90


def generate_tasks() -> GradeTasks:
    point_repository = PointRepository()
    senior_points_statement_1 = point_repository.get_destinations(le_days_after_delivery=8, lt_percent_completed_requests=100, point_completed=False)
    senior_points_statement_2 = point_repository.get_destinations(le_days_after_delivery=15, point_completed=False)
    senior_points = list(set().union(senior_points_statement_1, senior_points_statement_2))

    middle_points = point_repository.get_destinations(lt_percent_completed_requests=50, point_completed=False)

    junior_points_statement_1 = point_repository.get_destinations(ge_created_at=date.today() - timedelta(days=1), point_completed=False)
    junior_points_statement_2 = point_repository.get_destinations(is_delivered=False, point_completed=False)
    junior_points = list(set().union(junior_points_statement_1, junior_points_statement_2))

    senior_tasks = [
        Task(
            point=Point.model_validate(point.point),
            priority=PriorityEnum.HIGH,
            duration_work=SENIOR_TASKS_DURATION_MINUTES,
        )
        for point in senior_points
    ]
    middle_tasks = [
        Task(
            point=Point.model_validate(point.point),
            priority=PriorityEnum.MIDDLE,
            duration_work=MIDDLE_TASKS_DURATION_MINUTES,
        )
        for point in middle_points
    ]
    junior_tasks = [
        Task(
            point=Point.model_validate(point.point),
            priority=PriorityEnum.LOW,
            duration_work=JUNIOR_TASKS_DURATION_MINUTES,
        )
        for point in junior_points
    ]

    return GradeTasks(
        junior_tasks=junior_tasks,
        middle_tasks=middle_tasks,
        senior_tasks=senior_tasks,
    )


def generate_graph(tasks: GradeTasks) -> dict:
    point_repository = PointRepository()
    graph = defaultdict(dict)
    all_tasks = tasks.senior + tasks.middle + tasks.junior
    workplaces = point_repository.get_workplaces()

    for workplace in workplaces:
        for task in all_tasks:
            graph[workplace.point.id][task.point.id] = GraphElement(
                duration=point_repository.get_points_duration(workplace.point.id, task.point.id),
                task=task,
            )

    for from_task in all_tasks:
        for to_task in all_tasks:
            if from_task is not to_task:
                graph[from_task.point.id][to_task.point.id] = GraphElement(
                    duration=point_repository.get_points_duration(from_task.point.id, to_task.point.id),
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


def save_tasks_by_workers(distributed_tasks_by_workers: dict):
    # TODO: Add models in database and realize save
    return None


@celery.task(name='tasks_distribution')
def tasks_distribution():
    point_repository = UserRepository()
    tasks_by_grade = generate_tasks()
    graph = generate_graph()
    tasks_for_grade = {
        grade: get_available_tasks(grade=grade, tasks=tasks_by_grade) for grade in [WorkerGradeEnum.SENIOR, WorkerGradeEnum.MIDDLE, WorkerGradeEnum.JUNIOR]
    }

    distributed_tasks_by_workers = {}
    workers = point_repository.get_workers()
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

    save_tasks_by_workers(distributed_tasks_by_workers)
