from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from internal.repositories.db.models.point import Point
from internal.repositories.db.points import PointRepository
from internal.tasks import load_durations_for_workplace


class PointService:
    def __init__(self):
        self.point_repository = PointRepository()

    async def add_workplace(self, address: str, city: str) -> UUID:
        try:
            point = await self.point_repository.add_point(address=address, city=city)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Point already exists') from e

        try:
            workplace = await self.point_repository.add_workplace(point_id=point.id)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Workplace already exists') from e

        load_durations_for_workplace.delay(workplace.point_id, city, address)

        return workplace.point_id

    async def get_workplace(self, point_id: UUID) -> dict:
        workplace = await self.point_repository.get_workplace(point_id=point_id)
        return form_point_response(workplace.point)

    async def get_workplaces(self) -> list:
        workplaces = await self.point_repository.get_workplaces()
        data = [form_point_response(place.point) for place in workplaces]
        return data


def form_point_response(point: Point):
    response = {'id': point.id, 'address': point.address, 'city': point.city}
    return response
