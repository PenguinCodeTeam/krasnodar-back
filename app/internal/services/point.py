from uuid import UUID

from fastapi.exceptions import HTTPException

from internal.repositories.db.points import PointRepository
from sqlalchemy.exc import IntegrityError


class PointService:
    def __init__(self):
        self.repository = PointRepository()

    async def add_workplace(self, address: str, latitude: float, longitude: float) -> UUID:
        try:
            point = await self.repository.add_point(address, latitude, longitude)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Point already exists') from e

        try:
            workplace = await self.repository.add_workplace(point.id)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Workplace already exists') from e

        return workplace.point_id

    async def get_workplace(self, point_id: UUID) -> dict:
        workplace = await self.repository.get_workplace(point_id)
        point = workplace.point
        result = {'id': point.id, 'address': point.address, 'latitude': point.latitude, 'longitude': point.longitude}
        return result

    async def get_workplaces(self) -> list:
        workplaces = await self.repository.get_workplaces()
        data = []
        for place in workplaces:
            point = place.point
            data.append({'id': point.id, 'address': point.address, 'latitude': point.latitude, 'longitude': point.longitude})
        return data
