import datetime
import uuid

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from internal.core.types import PriorityEnum, TaskStatusEnum, WorkerGradeEnum
from internal.repositories.db.models.base import Base
from internal.repositories.db.models.point import Point
from internal.repositories.db.models.user import Worker


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    task_type_id: Mapped[int] = mapped_column(ForeignKey('task_types.id'))
    point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('points.id'))
    status: Mapped[TaskStatusEnum] = mapped_column(Enum(TaskStatusEnum), default=TaskStatusEnum.OPEN)

    point: Mapped[Point] = relationship(lazy='joined')
    task_type: Mapped['TaskType'] = relationship(lazy='joined')


class TaskType(Base):
    __tablename__ = 'task_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    priority: Mapped[PriorityEnum] = mapped_column(Enum(PriorityEnum))
    duration: Mapped[int]

    task_grades: Mapped[list['TaskGrade']] = relationship(lazy='joined', back_populates='task_type')


class TaskGrade(Base):
    __tablename__ = 'task_grades'

    task_type_id: Mapped[int] = mapped_column(ForeignKey('task_types.id'), primary_key=True)
    grade: Mapped[WorkerGradeEnum] = mapped_column(Enum(WorkerGradeEnum), primary_key=True)

    task_type: Mapped[TaskType] = relationship(lazy='joined', back_populates='task_grades')


class WorkSchedule(Base):
    __tablename__ = 'work_schedule'

    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('tasks.id'), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('workers.user_id'))
    date: Mapped[datetime.date] = mapped_column(default=datetime.date.today)
    task_number: Mapped[int]
    expected_start_at: Mapped[int]
    expected_finish_at: Mapped[int]
    started_at: Mapped[int | None]
    finished_at: Mapped[int | None]

    worker: Mapped[Worker] = relationship(lazy='joined')
    task: Mapped[Task] = relationship(lazy='joined')
