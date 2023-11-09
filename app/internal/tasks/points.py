import asyncio
from uuid import UUID

from config import OPEN_ROUTE_SERVICE_API_KEY, YANDEX_GEOCODER_API_KEY
from internal.repositories.db import PointRepository
from internal.repositories.open_route_service import OpenRouteServiceRepository
from internal.repositories.yandex_geocoder import YandexGeocoderRepository
from internal.tasks.worker import celery


async def async_load_durations_for_point(point_id: UUID, city: str, address: str, is_workplace: bool = False) -> None:
    point_repository = PointRepository()
    open_route_service = OpenRouteServiceRepository(api_key=OPEN_ROUTE_SERVICE_API_KEY)
    yandex_geocoder = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)
    point_coordinates = await yandex_geocoder.get_coordinates(city=city, address=address)
    destinations = [
        {
            'point_id': destination.point.id,
            'coordinates': await yandex_geocoder.get_coordinates(city=destination.point.city, address=destination.point.address),
        }
        for destination in await point_repository.get_destinations()
    ]
    for destination in destinations:
        to_destination_point_duration = await open_route_service.get_duration(point_coordinates, destination['coordinates'])
        point_repository.add_points_duration(point_id, destination['point_id'], to_destination_point_duration)
        if not is_workplace:
            from_destination_point_duration = await open_route_service.get_duration(destination['coordinates'], point_coordinates)
            point_repository.add_points_duration(destination['point_id'], point_id, from_destination_point_duration)
    if not is_workplace:
        workplaces = [
            {
                'point_id': destination.point.id,
                'coordinates': await yandex_geocoder.get_coordinates(city=workplace.point.city, address=workplace.point.address),
            }
            for workplace in await point_repository.get_workplaces()
        ]
        for workplace in workplaces:
            to_workplace_point_duration = await open_route_service.get_duration(point_coordinates, workplace['coordinates'])
            point_repository.add_points_duration(workplace['point_id'], point_id, to_workplace_point_duration)


@celery.task(name='load_durations_for_point')
def load_durations_for_point(point_id: UUID, city: str, address: str, is_workplace: bool = False):
    asyncio.get_event_loop().run_until_complete(async_load_durations_for_point(point_id, city, address, is_workplace))


async def load_durations_for_points(ignored_addresses: set[str]) -> None:
    point_repository = PointRepository()
    open_route_service = OpenRouteServiceRepository(api_key=OPEN_ROUTE_SERVICE_API_KEY)
    yandex_geocoder = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)
    destinations = [
        (
            await yandex_geocoder.get_coordinates(destination.point.city, destination.point.address),
            destination.point_id,
            f'{destination.point.city}, {destination.point.address}',
        )
        for destination in await point_repository.get_destinations()
    ]
    workplaces = [
        (
            await yandex_geocoder.get_coordinates(workplace.point.city, workplace.point.address),
            workplace.point_id,
            f'{workplace.point.city}, {workplace.point.address}',
        )
        for workplace in await point_repository.get_workplaces()
    ]
    for workplace_coordinates, workplace_id, workplace_full_address in workplaces:
        for destination_coordinates, destination_id, destination_full_address in destinations:
            if workplace_full_address in ignored_addresses and destination_full_address in ignored_addresses:
                continue
            duration = await open_route_service.get_duration(workplace_coordinates, destination_coordinates)
            await point_repository.add_points_duration(from_point_id=workplace_id, to_point_id=destination_id, duration=duration)
    for from_coordinates, from_id, from_full_address in destinations:
        for to_coordinates, to_id, to_full_address in destinations:
            if from_full_address in ignored_addresses and to_full_address in ignored_addresses or from_id == to_id:
                continue
            duration = await open_route_service.get_duration(from_coordinates, to_coordinates)
            await point_repository.add_points_duration(from_point_id=from_id, to_point_id=to_id, duration=duration)
