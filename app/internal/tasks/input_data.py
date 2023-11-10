import asyncio
import string
from datetime import date, timedelta
from random import choice

from config import YANDEX_GEOCODER_API_KEY
from internal.repositories.db import PointRepository
from internal.repositories.yandex_geocoder import YandexGeocoderRepository
from internal.tasks.points import load_durations_for_points
from internal.tasks.tasks import async_generate_tasks
from internal.tasks.worker import celery


# TODO: Заменить по возможности Exception


def get_result_form():
    return {
        'new': {
            'success': 0,
            'failed': 0,
            'success_data': [],
            'failed_data': [],
        },
        'updated': {
            'success': 0,
            'failed': 0,
            'success_data': [],
            'failed_data': [],
        },
    }


def generate_employee_id():
    letters = string.ascii_lowercase + string.digits
    return 'employee_' + ''.join(choice(letters) for _ in range(6))


def generate_employee_password():
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(choice(letters) for _ in range(8))


async def update_destinations(destinations: dict, city: str, point_repository: PointRepository, yandex_geocoder: YandexGeocoderRepository):
    result = []
    storaged_destinations = await point_repository.get_destinations()
    new_destination_by_addresses = {city + ', ' + destination['address']: destination for destination in destinations}
    for destination in storaged_destinations:
        if f'{destination.point.city}, {destination.point.address}' in new_destination_by_addresses.keys():
            new_destination = new_destination_by_addresses[f'{destination.point.city}, {destination.point.address}']
            new_destination['point_id'] = destination.point_id
            new_destination['created_at'] = date.today() - timedelta(days=1) if new_destination['connected_at'] == 'вчера' else date(day=1, month=1, year=2000)
            new_destination['full_address'] = 'г. ' + f'{destination.point.city}, {destination.point.address}'
            try:
                await point_repository.update_destination(
                    destination,
                    created_at=new_destination['created_at'],
                    is_delivered=new_destination['is_delivered'],
                    days_after_delivery=new_destination['days_after_delivery'],
                    accepted_requests=new_destination['accepted_requests'],
                    completed_requests=new_destination['completed_requests'],
                )
                result.append(new_destination)
            except Exception:
                pass
            new_destination_by_addresses.pop(f'{destination.point.city}, {destination.point.address}')
    for destination in destinations:
        if city + ', ' + destination['address'] in new_destination_by_addresses.keys():
            destination['created_at'] = date.today() - timedelta(days=1) if destination['connected_at'] == 'вчера' else date(day=1, month=1, year=2000)
            destination['full_address'] = 'г. ' + city + ', ' + destination['address']
            try:
                if not await yandex_geocoder.get_coordinates(city=city, address=destination['address']):
                    raise Exception()
                point = await point_repository.add_point(city=city, address=destination['address'])
                await point_repository.add_destination(
                    point_id=point.id,
                    created_at=destination['created_at'],
                    is_delivered=destination['is_delivered'],
                    days_after_delivery=destination['days_after_delivery'],
                    accepted_requests=destination['accepted_requests'],
                    completed_requests=destination['completed_requests'],
                )
                destination['point_id'] = point.id
                result.append(destination)
            except Exception:
                pass
    return result


async def async_update_input_data(destinations: dict, city: str, for_date: date):
    yandex_geocoder = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)
    point_repository = PointRepository()

    destinations_result = await update_destinations(destinations, city, point_repository, yandex_geocoder)
    destination_ids = [destination['point_id'] for destination in destinations_result]

    await load_durations_for_points()
    await async_generate_tasks(destination_ids, for_date)

    return {
        'destinations': destinations_result,
    }


@celery.task(name='update_input_data')
def update_input_data(destinations: dict, city: str, for_date: date):
    return asyncio.get_event_loop().run_until_complete(async_update_input_data(destinations, city, for_date))
