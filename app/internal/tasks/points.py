import asyncio
from uuid import UUID

from config import OPEN_ROUTE_SERVICE_API_KEY
from internal.repositories.db import PointRepository
from internal.repositories.open_route_service import OpenRouteServiceRepository
from internal.tasks.worker import celery


@celery.task(name='load_durations_for_point')
def load_durations_for_point(point_id: UUID, point_coordinates: tuple[float], is_workplace: bool = False) -> None:
    point_repository = PointRepository()
    open_route_service = OpenRouteServiceRepository(api_key=OPEN_ROUTE_SERVICE_API_KEY)
    destinations = asyncio.run(point_repository.get_destinations())
    for destination in destinations:
        destination_point_coordinates = (destination.point.latitude, destination.point.longitude)
        to_destination_point_duration = asyncio.run(open_route_service.get_duration(point_coordinates, destination_point_coordinates))
        point_repository.add_points_duration(point_id, destination.point.id, to_destination_point_duration)
        if not is_workplace:
            from_destination_point_duration = asyncio.run(open_route_service.get_duration(destination_point_coordinates, point_coordinates))
            point_repository.add_points_duration(destination.point.id, point_id, from_destination_point_duration)
    if not is_workplace:
        workplaces = asyncio.run(point_repository.get_workplaces())
        for workplace in workplaces:
            workplace_point_coordinates = (workplace.point.latitude, workplace.point.longitude)
            to_workplace_point_duration = asyncio.run(open_route_service.get_duration(point_coordinates, workplace_point_coordinates))
            point_repository.add_points_duration(workplace.point.id, point_id, to_workplace_point_duration)
