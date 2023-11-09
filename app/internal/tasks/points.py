import asyncio
from math import ceil
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
    db_destinations = await point_repository.get_destinations()
    coordinates = []
    for attempt in range(int(ceil(len(db_destinations) / 50))):
        coordinate_tasks = [
            yandex_geocoder.get_coordinates(city=db_destinations[index].point.city, address=db_destinations[index].point.address)
            for index in range(attempt * 50, min((attempt + 1) * 50, len(db_destinations)))
        ]
        coordinates.extend(await asyncio.gather(*coordinate_tasks))
    destinations = [
        {
            'point_id': destination.point_id,
            'coordinates': coordinate,
        }
        for destination, coordinate in zip(db_destinations, coordinates)
    ]
    to_add_durations = []
    for destination in destinations:
        if destination['point_id'] == point_id:
            continue
        to_add_durations.append(
            {
                'from_point_id': point_id,
                'to_point_id': destination['point_id'],
                'duration': open_route_service.get_duration(point_coordinates, destination['coordinates']),
            }
        )
        if not is_workplace:
            to_add_durations.append(
                {
                    'from_point_id': destination['point_id'],
                    'to_point_id': point_id,
                    'duration': open_route_service.get_duration(destination['coordinates'], point_coordinates),
                }
            )

    if not is_workplace:
        db_workplaces = await point_repository.get_workplaces()
        coordinates = []
        for attempt in range(int(ceil(len(db_workplaces) / 50))):
            coordinate_tasks = [
                yandex_geocoder.get_coordinates(city=db_workplaces[index].point.city, address=db_workplaces[index].point.address)
                for index in range(attempt * 50, min((attempt + 1) * 50, len(db_workplaces)))
            ]
            coordinates.extend(await asyncio.gather(*coordinate_tasks))
        workplaces = [
            {
                'point_id': workplace.point_id,
                'coordinates': coordinate,
            }
            for workplace, coordinate in zip(db_workplaces, coordinates)
        ]
        for workplace in workplaces:
            to_add_durations.append(
                {
                    'from_point_id': workplace['point_id'],
                    'to_point_id': point_id,
                    'duration': open_route_service.get_duration(point_coordinates, workplace['coordinates']),
                }
            )

    durations = []
    for attempt in range(int(ceil(len(to_add_durations) / 40))):
        duration_tasks = [to_add_durations[index]['duration'] for index in range(attempt * 40, min((attempt + 1) * 40, len(to_add_durations)))]
        durations.extend(await asyncio.gather(*duration_tasks))
    for index in range(len(to_add_durations)):
        await point_repository.add_points_duration(
            from_point_id=to_add_durations[index]['from_point_id'], to_point_id=to_add_durations[index]['to_point_id'], duration=durations[index]
        )


@celery.task(name='load_durations_for_point')
def load_durations_for_point(point_id: UUID, city: str, address: str, is_workplace: bool = False):
    asyncio.get_event_loop().run_until_complete(async_load_durations_for_point(point_id, city, address, is_workplace))


async def load_durations_for_points(ignored_addresses: set[str]) -> None:
    point_repository = PointRepository()
    open_route_service = OpenRouteServiceRepository(api_key=OPEN_ROUTE_SERVICE_API_KEY)
    yandex_geocoder = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)

    db_destinations = await point_repository.get_destinations()
    coordinates = []
    for attempt in range(int(ceil(len(db_destinations) / 50))):
        coordinate_tasks = [
            yandex_geocoder.get_coordinates(city=db_destinations[index].point.city, address=db_destinations[index].point.address)
            for index in range(attempt * 50, min((attempt + 1) * 50, len(db_destinations)))
        ]
        coordinates.extend(await asyncio.gather(*coordinate_tasks))
    destinations = [
        (coordinate, destination.point_id, 'г. ' + f'{destination.point.city}, {destination.point.address}')
        for destination, coordinate in zip(db_destinations, coordinates)
    ]

    db_workplaces = await point_repository.get_workplaces()
    coordinates = []
    for attempt in range(int(ceil(len(db_workplaces) / 50))):
        coordinate_tasks = [
            yandex_geocoder.get_coordinates(city=db_workplaces[index].point.city, address=db_workplaces[index].point.address)
            for index in range(attempt * 50, min((attempt + 1) * 50, len(db_workplaces)))
        ]
        coordinates.extend(await asyncio.gather(*coordinate_tasks))
    workplaces = [
        (coordinate, workplace.point_id, 'г. ' + f'{workplace.point.city}, {workplace.point.address}')
        for workplace, coordinate in zip(db_workplaces, coordinates)
    ]

    to_add_durations = []
    for workplace_coordinates, workplace_id, workplace_full_address in workplaces:
        for destination_coordinates, destination_id, destination_full_address in destinations:
            if workplace_full_address in ignored_addresses and destination_full_address in ignored_addresses:
                continue
            to_add_durations.append(
                {
                    'from_point_id': workplace_id,
                    'to_point_id': destination_id,
                    'duration': open_route_service.get_duration(workplace_coordinates, destination_coordinates),
                }
            )

    for from_coordinates, from_id, from_full_address in destinations:
        for to_coordinates, to_id, to_full_address in destinations:
            if from_full_address in ignored_addresses and to_full_address in ignored_addresses or from_id == to_id:
                continue
            to_add_durations.append(
                {'from_point_id': from_id, 'to_point_id': to_id, 'duration': open_route_service.get_duration(from_coordinates, to_coordinates)}
            )

    durations = []
    for attempt in range(int(ceil(len(to_add_durations) / 40))):
        duration_tasks = [to_add_durations[index]['duration'] for index in range(attempt * 40, min((attempt + 1) * 40, len(to_add_durations)))]
        durations.extend(await asyncio.gather(*duration_tasks))
    for index in range(len(to_add_durations)):
        await point_repository.add_points_duration(
            from_point_id=to_add_durations[index]['from_point_id'], to_point_id=to_add_durations[index]['to_point_id'], duration=durations[index]
        )
