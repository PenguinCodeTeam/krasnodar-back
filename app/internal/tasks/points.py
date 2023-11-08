import asyncio
from uuid import UUID

from config import OPEN_ROUTE_SERVICE_API_KEY, YANDEX_GEOCODER_API_KEY
from internal.repositories.db import PointRepository
from internal.repositories.open_route_service import OpenRouteServiceRepository
from internal.repositories.yandex_geocoder import YandexGeocoderRepository
from internal.tasks.worker import celery


@celery.task(name='load_durations_for_point')
def load_durations_for_point(point_id: UUID, city: str, address: str, is_workplace: bool = False) -> None:
    point_repository = PointRepository()
    open_route_service = OpenRouteServiceRepository(api_key=OPEN_ROUTE_SERVICE_API_KEY)
    yandex_geocoder = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)
    point_coordinates = asyncio.run(yandex_geocoder.get_coordinates(city=city, address=address))
    destinations = [
        {
            'point_id': destination.point.id,
            'coordinates': asyncio.run(yandex_geocoder.get_coordinates(city=destination.point.city, address=destination.point.address)),
        }
        for destination in asyncio.run(point_repository.get_destinations())
    ]
    for destination in destinations:
        to_destination_point_duration = asyncio.run(open_route_service.get_duration(point_coordinates, destination['coordinates']))
        point_repository.add_points_duration(point_id, destination['point_id'], to_destination_point_duration)
        if not is_workplace:
            from_destination_point_duration = asyncio.run(open_route_service.get_duration(destination['coordinates'], point_coordinates))
            point_repository.add_points_duration(destination['point_id'], point_id, from_destination_point_duration)
    if not is_workplace:
        workplaces = [
            {
                'point_id': destination.point.id,
                'coordinates': asyncio.run(yandex_geocoder.get_coordinates(city=workplace.point.city, address=workplace.point.address)),
            }
            for workplace in asyncio.run(point_repository.get_workplaces())
        ]
        for workplace in workplaces:
            to_workplace_point_duration = asyncio.run(open_route_service.get_duration(point_coordinates, workplace['coordinates']))
            point_repository.add_points_duration(workplace['point_id'], point_id, to_workplace_point_duration)
