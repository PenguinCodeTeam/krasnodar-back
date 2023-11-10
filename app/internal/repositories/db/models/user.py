import datetime
import uuid

from sqlalchemy import Enum, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from internal.core.types import RoleEnum, WorkerGradeEnum
from internal.repositories.db.models.base import Base

from .point import Workplace


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, unique=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum))


class Worker(Base):
    __tablename__ = 'workers'

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('users.id'), primary_key=True)
    workplace_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('workplaces.point_id'))
    grade: Mapped[WorkerGradeEnum] = mapped_column(Enum(WorkerGradeEnum))

    user: Mapped[User] = relationship(lazy='joined')
    workplace: Mapped[Workplace] = relationship(lazy='joined')


class WorkingDate(Base):
    __tablename__ = 'working_date'

    worker_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('workers.user_id'), primary_key=True)
    date: Mapped[datetime.date] = mapped_column(primary_key=True)

    worker: Mapped[Worker] = relationship(lazy='joined')
