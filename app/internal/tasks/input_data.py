import asyncio
import string
from datetime import date, timedelta
from random import choice

from config import YANDEX_GEOCODER_API_KEY
from internal.core.types import RoleEnum
from internal.repositories.db import PointRepository, TaskRepository, UserRepository
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


async def update_destinations(destinations: dict, point_repository: PointRepository, yandex_geocoder: YandexGeocoderRepository):
    result = get_result_form()
    storaged_destinations = await point_repository.get_destinations()
    new_destination_by_addresses = {destination['city'] + ', ' + destination['address']: destination for destination in destinations}
    for destination in storaged_destinations:
        if f'{destination.point.city}, {destination.point.address}' in new_destination_by_addresses.keys():
            new_destination = new_destination_by_addresses[f'{destination.point.city}, {destination.point.address}']
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
                result['updated']['success'] += 1
                result['updated']['success_data'].append(new_destination)
            except Exception:
                result['updated']['failed'] += 1
                result['updated']['failed_data'].append(new_destination)
            new_destination_by_addresses.pop(f'{destination.point.city}, {destination.point.address}')
        else:
            await point_repository.delete_destination(destination)
            await point_repository.delete_points_durations(from_point_id=destination.point.id)
            await point_repository.delete_points_durations(to_point_id=destination.point.id)
            await point_repository.delete_point(destination.point)
    for destination in destinations:
        if destination['city'] + ', ' + destination['address'] in new_destination_by_addresses.keys():
            destination['created_at'] = date.today() - timedelta(days=1) if destination['connected_at'] == 'вчера' else date(day=1, month=1, year=2000)
            destination['full_address'] = 'г. ' + destination['city'] + ', ' + destination['address']
            try:
                if not await yandex_geocoder.get_coordinates(city=destination['city'], address=destination['address']):
                    raise Exception()
                point = await point_repository.add_point(city=destination['city'], address=destination['address'])
                await point_repository.add_destination(
                    point_id=point.id,
                    created_at=destination['created_at'],
                    is_delivered=destination['is_delivered'],
                    days_after_delivery=destination['days_after_delivery'],
                    accepted_requests=destination['accepted_requests'],
                    completed_requests=destination['completed_requests'],
                )
                result['new']['success'] += 1
                result['new']['success_data'].append(destination)
            except Exception:
                result['new']['failed'] += 1
                result['new']['failed_data'].append(destination)
    return result


async def update_task_types(task_types: dict, task_repository: TaskRepository):
    result = get_result_form()
    for task_type in task_types:
        try:
            db_task_type = await task_repository.get_task_type(name=task_type['name'])
            await task_repository.update_task_type(task_type=db_task_type, priority=task_type['priority'], duration=task_type['duration'])
            result['updated']['success'] += 1
            result['updated']['success_data'].append(task_type)
        except Exception:
            result['updated']['failed'] += 1
            result['updated']['failed_data'].append(task_type)
    return result


async def update_workplaces(workers: dict, point_repository: PointRepository, yandex_geocoder: YandexGeocoderRepository):
    result = get_result_form()
    storaged_workplaces = await point_repository.get_workplaces()
    new_workplaces_by_address = {worker['city'] + ', ' + worker['address'] for worker in workers}
    for workplace in storaged_workplaces:
        if f'{workplace.point.city}, {workplace.point.address}' in new_workplaces_by_address:
            new_workplaces_by_address.remove(f'{workplace.point.city}, {workplace.point.address}')
            result['updated']['success'] += 1
            result['updated']['success_data'].append({'full_address': 'г. ' + f'{workplace.point.city}, {workplace.point.address}'})
    for worker in workers:
        if worker['city'] + ', ' + worker['address'] in new_workplaces_by_address:
            try:
                if not await yandex_geocoder.get_coordinates(city=worker['city'], address=worker['address']):
                    raise Exception()
                point = await point_repository.add_point(city=worker['city'], address=worker['address'])
                await point_repository.add_workplace(point_id=point.id)
                new_workplaces_by_address.remove(worker['city'] + ', ' + worker['address'])
                result['new']['success'] += 1
                result['new']['success_data'].append({'full_address': 'г. ' + worker['city'] + ', ' + worker['address']})
            except Exception:
                result['new']['failed'] += 1
                result['new']['failed_data'].append({'full_address': 'г. ' + worker['city'] + ', ' + worker['address']})
    return result


async def update_workers(workers: dict, point_repository: PointRepository, user_repository: UserRepository):
    result = get_result_form()
    storaged_workers = await user_repository.get_workers()
    new_workers_by_names = {worker['surname'] + ' ' + worker['name'] + ' ' + worker['patronymic']: worker for worker in workers}
    for worker in storaged_workers:
        if f'{worker.user.surname} {worker.user.name} {worker.user.patronymic}' in new_workers_by_names.keys():
            update_worker = new_workers_by_names[f'{worker.user.surname} {worker.user.name} {worker.user.patronymic}']
            update_worker['login'] = worker.user.login
            update_worker['full_address'] = 'г. ' + f'{worker.workplace.point.city}, {worker.workplace.point.address}'
            new_workers_by_names.pop(f'{worker.user.surname} {worker.user.name} {worker.user.patronymic}')
            try:
                await user_repository.update_user(worker.user, login=update_worker['login'])
                await user_repository.update_worker(worker, grade=update_worker['grade'], is_active=True)
                result['updated']['success'] += 1
                result['updated']['success_data'].append(update_worker)
            except Exception:
                result['updated']['failed'] += 1
                result['updated']['failed_data'].append(update_worker)
        else:
            await user_repository.update_worker(worker, is_active=False)
    for worker in workers:
        if worker['surname'] + ' ' + worker['name'] + ' ' + worker['patronymic'] in new_workers_by_names.keys():
            worker['role'] = RoleEnum.EMPLOYEE
            worker['login'] = generate_employee_id()
            worker['password'] = generate_employee_password()
            worker['full_address'] = 'г. ' + worker['city'] + ', ' + worker['address']
            try:
                point = await point_repository.get_point(city=worker['city'], address=worker['address'])
                workplace = await point_repository.get_workplace(point_id=point.id)
                user = await user_repository.add_user(
                    login=worker['login'],
                    password=worker['password'],
                    name=worker['name'],
                    surname=worker['surname'],
                    patronymic=worker['patronymic'],
                    role=worker['role'],
                )
                await user_repository.add_worker(user_id=user.id, workplace_id=workplace.point_id, grade=worker['grade'])
                result['new']['success'] += 1
                result['new']['success_data'].append(worker)
            except Exception:
                if 'login' in worker:
                    worker.pop('login')
                if 'password' in worker:
                    worker.pop('password')
                result['new']['failed'] += 1
                result['new']['failed_data'].append(worker)
    return result


async def async_update_input_data(destinations: dict, task_types: dict, workers: dict):
    yandex_geocoder = YandexGeocoderRepository(api_key=YANDEX_GEOCODER_API_KEY)
    point_repository = PointRepository()
    task_repository = TaskRepository()
    user_repository = UserRepository()

    await task_repository.delete_tasks()

    destinations_result = await update_destinations(destinations, point_repository, yandex_geocoder)
    ignored_destinations = {point['full_address'] for point in destinations_result['updated']['success_data'] + destinations_result['updated']['failed_data']}
    task_types_result = await update_task_types(task_types, task_repository)
    workplaces_result = await update_workplaces(workers, point_repository, yandex_geocoder)
    ignored_workplaces = {point['full_address'] for point in workplaces_result['updated']['success_data'] + workplaces_result['updated']['failed_data']}
    workers_result = await update_workers(workers, point_repository, user_repository)
    ignored_addresses = set().union(ignored_destinations, ignored_workplaces)

    await load_durations_for_points(ignored_addresses)
    await async_generate_tasks()

    return {
        'destinations': destinations_result,
        'task_types': task_types_result,
        'workplaces': workplaces_result,
        'workers': workers_result,
    }


@celery.task(name='update_input_data')
def update_input_data(destinations: dict, task_types: dict, workers: dict):
    return asyncio.get_event_loop().run_until_complete(async_update_input_data(destinations, task_types, workers))
