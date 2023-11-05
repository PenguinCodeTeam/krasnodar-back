import uuid
from datetime import date

from internal.repositories.db.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Point(Base):
    __tablename__ = 'points'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, unique=True)
    address: Mapped[str] = mapped_column(primary_key=True)
    latitude: Mapped[float]
    longitude: Mapped[float]


class Destination(Base):
    __tablename__ = 'destinations'

    point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('points.id'), primary_key=True)
    created_at: Mapped[date] = mapped_column(default=date.today)
    is_delivered: Mapped[bool]
    days_after_delivery: Mapped[int]
    accepted_requests: Mapped[int]
    completed_requests: Mapped[int]

    @hybrid_property
    def percent_completed_requests(self):
        return self.completed_requests / self.accepted_requests * 100

    point: Mapped[Point] = relationship(lazy='joined')


class Workplace(Base):
    __tablename__ = 'workplaces'

    point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('points.id'), primary_key=True)

    point: Mapped[Point] = relationship(lazy='joined')


class PointsDuration(Base):
    __tablename__ = 'points_distance'

    from_point_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    to_point_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    duration: Mapped[int]
