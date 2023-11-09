import uuid
import zoneinfo
from datetime import date, datetime
from typing import Type

from sqlalchemy import delete, select

from internal.core.types import Empty, PriorityEnum, TaskStatusEnum, WorkerGradeEnum
from internal.repositories.db.base import DatabaseRepository
from internal.repositories.db.models import Task, TaskGrade, TaskType, WorkSchedule


START_WORKING_DAY_TIME = 9 * 60 * 60  # 9 hours


class TaskRepository(DatabaseRepository):
    async def delete_tasks(self):
        query = delete(Task)
        async with self.transaction() as session:
            await session.execute(query)

    async def get_task_type(
        self,
        task_type_id: int | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
    ) -> TaskType | None:
        filters = []
        if task_type_id is not Empty:
            filters.append(TaskType.id == task_type_id)
        if name is not Empty:
            filters.append(TaskType.name == name)

        query = select(TaskType).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalar_one_or_none()

    async def get_task_types(self) -> tuple[TaskType]:
        query = select(TaskType)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalars().all()

    async def update_task_type(
        self,
        task_type: TaskType,
        priority: PriorityEnum | Type[Empty] = Empty,
        duration: int | Type[Empty] = Empty,
    ) -> TaskType:
        if priority is not Empty:
            task_type.priority = priority
        if duration is not Empty:
            task_type.duration = duration

        async with self.transaction() as session:
            session.add(task_type)

        return task_type

    async def get_task(
        self,
        task_type_id: uuid.UUID | Type[Empty],
        point_id: uuid.UUID | Type[Empty],
    ) -> Task | None:
        filters = []
        if task_type_id is not Empty:
            filters.append(Task.task_type_id == task_type_id)
        if point_id is not Empty:
            filters.append(Task.point_id == point_id)

        query = select(Task).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalar_one_or_none()

    async def get_tasks(
        self,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
        priority: PriorityEnum | Type[Empty] = Empty,
        status: TaskStatusEnum | Type[Empty] = Empty,
    ) -> tuple[Task]:
        filters = []
        if grade is not Empty:
            task_grade_query = select(TaskGrade.task_type_id).where(TaskGrade.grade == grade)
            filters.append(Task.task_type_id.in_(task_grade_query))
        if priority is not Empty:
            task_type_query = select(TaskType.id).where(TaskType.priority == priority)
            filters.append(Task.task_type_id.in_(task_type_query))
        if status is not Empty:
            filters.append(Task.status == status)

        query = select(Task).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalars().all()

    async def add_task(
        self,
        task_type_id: uuid.UUID,
        point_id: uuid.UUID,
    ) -> Task:
        task = Task(task_type_id=task_type_id, point_id=point_id)
        async with self.transaction() as session:
            session.add(task)

        return task

    async def add_work_schedule(self, user_id: uuid.UUID, route: list[dict]) -> list[WorkSchedule]:
        db_tasks = []
        moscow_timezone = zoneinfo.ZoneInfo('Europe/Moscow')
        date_object = date.today()
        datetime_object = datetime.datetime(date_object.year, date_object.month, date_object.day, tzinfo=moscow_timezone)
        expected_start_at = int(datetime_object.timestamp()) + START_WORKING_DAY_TIME
        for number, data in zip(range(1, len(route)), route):
            expected_finish_at = expected_start_at + data['duration_to_task'] + data['task'].task_type.duration
            db_tasks.append(
                WorkSchedule(
                    user_id=user_id, task_id=route['task'].id, task_number=number, expected_start_at=expected_start_at, expected_finish_at=expected_finish_at
                )
            )
            expected_start_at = expected_finish_at
        async with self.transaction() as session:
            session.add_all(db_tasks)

        return db_tasks
