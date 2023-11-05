import uuid
from datetime import date
from typing import Type

from internal.core.types import Empty
from internal.repositories.db.base import DatabaseRepository
from internal.repositories.db.models import Destination, Point, PointsDuration, Workplace
from sqlalchemy import select


class PointRepository(DatabaseRepository):
    async def get_point(
        self,
        id: uuid.UUID | Type[Empty] = Empty,
        address: str | Type[Empty] = Empty,
    ) -> Point | None:
        filters = []
        if id is not Empty:
            filters.append(Point.id == id)
        if address is not Empty:
            filters.append(Point.address == address)

        query = select(Point).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalar_one_or_none()

    async def get_points(self) -> list[Point]:
        query = select(Point)
        async with self.transaction() as session:
            res = await session.execute(query)

        return list(res.scalars().all())

    async def add_point(
        self,
        address: str,
        latitude: float,
        longitude: float,
    ) -> Point:
        user = Point(
            address=address,
            latitude=latitude,
            longitude=longitude,
        )
        async with self.transaction() as session:
            session.add(user)

        return user

    async def update_point(
        self,
        point: Point,
        address: str | Type[Empty] = Empty,
        latitude: float | Type[Empty] = Empty,
        longitude: float | Type[Empty] = Empty,
    ) -> Point:
        if address is not Empty:
            point.address = address
        if latitude is not Empty:
            point.latitude = latitude
        if longitude is not Empty:
            point.longitude = longitude

        async with self.transaction() as session:
            session.add(point)

        return point

    async def delete_point(
        self,
        point: Point,
    ) -> Point:
        async with self.transaction() as session:
            session.delete(point)

        return point

    async def get_workplace(self, point_id: uuid.UUID) -> Workplace | None:
        query = select(Workplace).where(Workplace.point_id == point_id)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalar_one_or_none()

    async def get_workplaces(self) -> list[Workplace]:
        query = select(Workplace)
        async with self.transaction() as session:
            res = await session.execute(query)

        return list(res.unique().scalars().all())

    async def add_workplace(self, point_id: uuid.UUID) -> Workplace:
        workplace = Workplace(point_id=point_id)
        async with self.transaction() as session:
            session.add(workplace)

        return workplace

    async def delete_workplace(self, workplace: Workplace) -> Workplace:
        async with self.transaction() as session:
            session.delete(workplace)

        return workplace

    async def get_destination(self, point_id: uuid.UUID) -> Destination | None:
        query = select(Destination).where(Destination.point_id == point_id)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalar_one_or_none()

    async def get_destinations(
        self,
        le_created_at: date | Type[Empty] = Empty,
        is_delivered: bool | Type[Empty] = Empty,
        le_days_after_delivery: int | Type[Empty] = Empty,
        ge_days_after_delivery: int | Type[Empty] = Empty,
        le_accepted_requests: int | Type[Empty] = Empty,
        ge_accepted_requests: int | Type[Empty] = Empty,
        le_completed_requests: int | Type[Empty] = Empty,
        ge_completed_requests: int | Type[Empty] = Empty,
        le_percent_completed_requests: float | Type[Empty] = Empty,
        ge_percent_completed_requests: float | Type[Empty] = Empty,
        point_completed: bool | Type[Empty] = Empty,
    ) -> list[Workplace]:
        filters = []
        if le_created_at is not Empty:
            filters.append(Destination.created_at <= le_created_at)
        if is_delivered is not Empty:
            filters.append(Destination.is_delivered == is_delivered)
        if le_days_after_delivery is not Empty:
            filters.append(Destination.days_after_delivery <= le_days_after_delivery)
        if ge_days_after_delivery is not Empty:
            filters.append(Destination.days_after_delivery >= ge_days_after_delivery)
        if le_accepted_requests is not Empty:
            filters.append(Destination.accepted_requests <= le_accepted_requests)
        if ge_accepted_requests is not Empty:
            filters.append(Destination.accepted_requests >= ge_accepted_requests)
        if le_completed_requests is not Empty:
            filters.append(Destination.completed_requests <= le_completed_requests)
        if ge_completed_requests is not Empty:
            filters.append(Destination.completed_requests >= ge_completed_requests)
        if le_percent_completed_requests is not Empty:
            filters.append(Destination.percent_completed_requests <= le_percent_completed_requests)
        if ge_percent_completed_requests is not Empty:
            filters.append(Destination.percent_completed_requests >= ge_percent_completed_requests)
        if point_completed is not Empty:
            filters.append(Destination.point_completed == point_completed)

        query = select(Destination).where(*filter)
        async with self.transaction() as session:
            res = await session.execute(query)

        return list(res.unique().scalars().all())

    async def add_destination(
        self,
        point_id: uuid.UUID,
        created_at: date,
        is_delivered: bool,
        days_after_delivery: int,
        accepted_requests: int,
        completed_requests: int,
    ) -> Destination:
        destination = Destination(
            point_id=point_id,
            created_at=created_at,
            is_delivered=is_delivered,
            days_after_delivery=days_after_delivery,
            accepted_requests=accepted_requests,
            completed_requests=completed_requests,
        )
        async with self.transaction() as session:
            session.add(destination)

        return destination

    async def update_destination(
        self,
        destination: Destination,
        created_at: date | Type[Empty] = Empty,
        is_delivered: bool | Type[Empty] = Empty,
        days_after_delivery: int | Type[Empty] = Empty,
        accepted_requests: int | Type[Empty] = Empty,
        completed_requests: int | Type[Empty] = Empty,
    ) -> Destination:
        if created_at is not Empty:
            destination.created_at = created_at
        if is_delivered is not Empty:
            destination.is_delivered = is_delivered
        if days_after_delivery is not Empty:
            destination.days_after_delivery = days_after_delivery
        if accepted_requests is not Empty:
            destination.accepted_requests = accepted_requests
        if completed_requests is not Empty:
            destination.completed_requests = completed_requests

        async with self.transaction() as session:
            session.add(destination)

        return destination

    async def delete_destination(self, destination: Destination) -> Destination:
        async with self.transaction() as session:
            session.delete(destination)

        return destination

    async def get_points_duration(self, from_point_id: uuid.UUID, to_point_id: uuid.UUID) -> PointsDuration | None:
        query = select(PointsDuration).where(
            PointsDuration.from_point_id == from_point_id,
            PointsDuration.to_point_id == to_point_id,
        )
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalar_one_or_none()

    async def get_points_durations(
        self,
        from_point_id: uuid.UUID | Type[Empty] = Empty,
        to_point_id: uuid.UUID | Type[Empty] = Empty,
        le_duration: int | Type[Empty] = Empty,
        ge_duration: int | Type[Empty] = Empty,
    ) -> list[PointsDuration]:
        filters = []
        if from_point_id is not Empty:
            filters.append(PointsDuration.from_point_id == from_point_id)
        if to_point_id is not Empty:
            filters.append(PointsDuration.to_point_id == to_point_id)
        if le_duration is not Empty:
            filters.append(PointsDuration.duration <= le_duration)
        if ge_duration is not Empty:
            filters.append(PointsDuration.duration >= ge_duration)

        query = select(PointsDuration).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return list(res.scalars().all())

    async def add_points_duration(self, from_point_id: uuid.UUID, to_point_id: uuid.UUID, duration: int) -> PointsDuration:
        points_duration = PointsDuration(from_point_id=from_point_id, to_point_id=to_point_id, duration=duration)

        async with self.transaction() as session:
            session.add(points_duration)

        return points_duration

    async def update_points_duration(
        self,
        points_duration: PointsDuration,
        from_point_id: uuid.UUID | Type[Empty] = Empty,
        to_point_id: uuid.UUID | Type[Empty] = Empty,
        duration: int | Type[Empty] = Empty,
    ) -> PointsDuration:
        if from_point_id is not Empty:
            points_duration.from_point_id = from_point_id
        if to_point_id is not Empty:
            points_duration.to_point_id = to_point_id
        if duration is not Empty:
            points_duration.duration = duration

        async with self.transaction() as session:
            session.add(points_duration)

        return points_duration

    async def delete_points_duration(self, points_duration: PointsDuration) -> PointsDuration:
        async with self.transaction() as session:
            session.delete(points_duration)

        return points_duration
