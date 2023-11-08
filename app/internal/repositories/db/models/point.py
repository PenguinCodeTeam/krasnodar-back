import uuid
from datetime import date

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from internal.repositories.db.models.base import Base


class Point(Base):
    __tablename__ = 'points'

    id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, primary_key=True, unique=True)
    address: Mapped[str]
    city: Mapped[str]
    __table_args__ = (UniqueConstraint('address', 'city', name='city_address_unique'),)


class Destination(Base):
    __tablename__ = 'destinations'

    point_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('points.id'), primary_key=True)
    created_at: Mapped[date] = mapped_column(default=date.today)
    is_delivered: Mapped[bool]
    days_after_delivery: Mapped[int]
    accepted_requests: Mapped[int]
    completed_requests: Mapped[int]
    point_completed: Mapped[bool] = mapped_column(default=False)

    @hybrid_property
    def percent_completed_requests(self) -> float:
        if self.accepted_requests == 0:
            return 100.0
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
