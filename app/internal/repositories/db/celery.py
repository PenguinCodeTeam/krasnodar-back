import uuid

from sqlalchemy import select

from internal.repositories.db.base import DatabaseRepository
from internal.repositories.db.models import CeleryTask


class CeleryTaskRepository(DatabaseRepository):
    async def get_task(self, task_name: str) -> CeleryTask | None:
        query = select(CeleryTask).where(CeleryTask.task_name == task_name)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalar_one_or_none()

    async def update_task(self, task_id: uuid.UUID, task_name: str):
        task = await self.get_task(task_name=task_name)

        if task:
            task.id = task_id
        else:
            task = CeleryTask(id=task_id, task_name=task_name)

        async with self.transaction() as session:
            session.add(task)

        return task
