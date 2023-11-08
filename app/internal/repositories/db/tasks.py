import uuid
from typing import Type

from sqlalchemy import select

from internal.core.types import Empty, PriorityEnum, TaskStatusEnum, WorkerGradeEnum
from internal.repositories.db.base import DatabaseRepository
from internal.repositories.db.models import Task, TaskGrade, TaskType, WorkSchedule


class TaskRepository(DatabaseRepository):
    async def get_task_type(
        self,
        task_type_id: uuid.UUID | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
    ) -> TaskType | None:
        filters = []
        if task_type_id is not Empty:
            filters.append(TaskType.id == task_type_id)
        if name is not Empty:
            filters.append(TaskType.login == name)

        query = select(TaskType).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalar_one_or_none()

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

    async def add_work_schedule(self, user_id: uuid.UUID, route: list[dict]) -> list[WorkSchedule]:
        db_tasks = []
        expected_start_at = 0
        for number, data in zip(range(1, len(route)), route):
            expected_finish_at = expected_start_at + route['duration_to_task'] + route['task'].task_type.duration
            db_tasks.append(
                WorkSchedule(
                    user_id=user_id, task_id=route['task'].id, task_number=number, expected_start_at=expected_start_at, expected_finish_at=expected_finish_at
                )
            )
            expected_start_at = expected_finish_at
        async with self.transaction() as session:
            session.add_all(db_tasks)

        return db_tasks
