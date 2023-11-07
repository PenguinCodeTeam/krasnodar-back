from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from config import YANDEX_GEOCODER_API_KEY
from internal.repositories.db.models.point import Point
from internal.repositories.db.points import PointRepository
from internal.repositories.yandex_geocoder import YandexGeocoderRepository
from internal.tasks import load_durations_for_point


class PointService:
    def __init__(self):
        self.point_repository = PointRepository()
        self.yandex_geocoder_repository = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)

    async def add_workplace(self, address: str) -> UUID:
        coordinates = await self.yandex_geocoder_repository.get_coordinates(city='Краснодар', address=address)

        try:
            point = await self.point_repository.add_point(address=address, latitude=coordinates[0], longitude=coordinates[1])
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Point already exists') from e

        try:
            workplace = await self.point_repository.add_workplace(point_id=point.id)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Workplace already exists') from e

        load_durations_for_point.delay(workplace.point_id, coordinates, True)

        return workplace.point_id

    async def get_workplace(self, point_id: UUID) -> dict:
        workplace = await self.point_repository.get_workplace(point_id=point_id)
        return form_point_response(workplace.point)

    async def get_workplaces(self) -> list:
        workplaces = await self.point_repository.get_workplaces()
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
