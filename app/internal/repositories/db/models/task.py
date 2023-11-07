import uuid
from datetime import date

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from internal.core.types import PriorityEnum
from internal.repositories.db.models.base import Base
from internal.repositories.db.models.point import Point
from internal.repositories.db.models.user import Worker


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[PriorityEnum] = mapped_column(Enum(PriorityEnum))
    duration: Mapped[int]
    for_junior: Mapped[bool] = mapped_column(default=True)
    for_middle: Mapped[bool] = mapped_column(default=True)
    for_senior: Mapped[bool] = mapped_column(default=True)


class ScheduleTask(Base):
    __tablename__ = 'schedule_tasks'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    worker_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('workers.user_id'))
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tasks.id'))
    working_date: Mapped[date] = mapped_column(default=date.today)
    number_task: Mapped[int]
    point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('points.id'))

    worker: Mapped[Worker] = relationship(lazy='joined')
    task: Mapped[Task] = relationship(lazy='joined')
    point: Mapped[Point] = relationship(lazy='joined')
