from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from internal.repositories.db.models.point import Point
from internal.repositories.db.points import PointRepository


class PointService:
    def __init__(self):
        self.repository = PointRepository()

    async def add_workplace(self, address: str, latitude: float, longitude: float) -> UUID:
        try:
            point = await self.repository.add_point(address=address, latitude=latitude, longitude=longitude)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Point already exists') from e

        try:
            workplace = await self.repository.add_workplace(point_id=point.id)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Workplace already exists') from e

        return workplace.point_id

    async def get_workplace(self, point_id: UUID) -> dict:
        workplace = await self.repository.get_workplace(point_id=point_id)
        return form_point_response(workplace.point)

    async def get_workplaces(self) -> list:
        workplaces = await self.repository.get_workplaces()
        data = [form_point_response(place.point) for place in workplaces]
        return data


def form_point_response(point: Point):
    response = {
        'id': point.id,
        'address': point.address,
        'latitude': point.latitude,
        'longitude': point.longitude,
    }
    return response
