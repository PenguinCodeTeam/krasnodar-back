import uuid
from typing import Type

from sqlalchemy import select

from internal.core.types import Empty, PriorityEnum, WorkerGradeEnum
from internal.repositories.db.base import DatabaseRepository
from internal.repositories.db.models import ScheduleTask, Task


class TaskRepository(DatabaseRepository):
    async def get_task(
        self,
        task_id: uuid.UUID | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
    ) -> Task | None:
        filters = []
        if task_id is not Empty:
            filters.append(Task.id == task_id)
        if name is not Empty:
            filters.append(Task.login == name)

        query = select(Task).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalar_one_or_none()

    async def get_tasks(
        self,
        priority: PriorityEnum | Type[Empty] = Empty,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
    ) -> tuple[Task]:
        filters = []
        if priority is not Empty:
            filters.append(Task.priority == priority)
        match grade:
            case WorkerGradeEnum.JUNIOR:
                filters.append(Task.for_junior.is_(True))
            case WorkerGradeEnum.MIDDLE:
                filters.append(Task.for_middle.is_(True))
            case WorkerGradeEnum.SENIOR:
                filters.append(Task.for_senior.is_(True))
            case _:
                pass

        query = select(Task).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalars().all()

    async def update_task(
        self,
        task: Task,
        duration: int | Type[Empty] = Empty,
        priority: PriorityEnum | Type[Empty] = Empty,
        grades: list[WorkerGradeEnum] | Type[Empty] = Empty,
    ) -> Task:
        if duration is not Empty:
            task.duration = duration
        if priority is not Empty:
            task.priority = priority

        if grades is not Empty:
            task.for_junior = False
            task.for_middle = False
            task.for_senior = False
            for grade in grades:
                match grade:
                    case WorkerGradeEnum.JUNIOR:
                        task.for_junior = True
                    case WorkerGradeEnum.MIDDLE:
                        task.for_middle = True
                    case WorkerGradeEnum.SENIOR:
                        task.for_senior = True
                    case _:
                        pass

        async with self.transaction() as session:
            session.add(task)

        return task

    async def add_schedule_tasks(self, worker_id: uuid.UUID, tasks: list) -> list[ScheduleTask]:
        db_tasks = [Task(worker_id=worker_id, task_id=task.id, number_task=number, point_id=task.point.id) for number, task in zip(range(len(tasks)), tasks)]
        async with self.transaction() as session:
            session.add_all(db_tasks)
        return db_tasks
