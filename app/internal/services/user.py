from typing import Type
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from internal.core.types import Empty, RoleEnum, WorkerGradeEnum
from internal.repositories.db.models.point import Point
from internal.repositories.db.models.user import User, Worker
from internal.repositories.db.points import PointRepository
from internal.repositories.db.users import UserRepository
from internal.tasks import load_durations_for_workplace


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.point_repository = PointRepository()

    async def create_manager(self, login: str, password: str, name: str, surname: str, patronymic: str) -> UUID:
        try:
            user = await self.user_repository.add_user(login=login, password=password, name=name, surname=surname, patronymic=patronymic, role=RoleEnum.MANAGER)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='User already exists') from e
        return user.id

    async def create_employee(
        self, login: str, password: str, name: str, surname: str, patronymic: str, address: str, city: str, grade: WorkerGradeEnum
    ) -> UUID:
        try:
            user = await self.user_repository.add_user(
                login=login, password=password, name=name, surname=surname, patronymic=patronymic, role=RoleEnum.EMPLOYEE
            )
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='User already exists') from e

        point = await self.point_repository.get_point(city=city, address=address)
        if not point:
            point = await self.point_repository.add_point(city=city, address=address)

        workplace = await self.point_repository.get_workplace(point_id=point.id)
        if not workplace:
            workplace = await self.point_repository.add_workplace(point_id=point.id)
            load_durations_for_workplace.delay(workplace.point_id, city, address)

        employee = await self.user_repository.add_worker(user_id=user.id, workplace_id=workplace.point_id, grade=grade)

        return employee.user_id

    async def get_employees(self) -> list:
        employees = await self.user_repository.get_workers()
        return [form_employee_response(worker) for worker in employees]

    async def get_employee(self, user_id: UUID) -> dict:
        worker = await self.user_repository.get_worker(user_id=user_id)
        if not worker:
            raise HTTPException(status_code=404, detail='Employee not found')

        return form_employee_response(worker)

    async def get_managers(self) -> list:
        users = await self.user_repository.get_users(role=RoleEnum.MANAGER)
        return [form_manager_response(manager) for manager in users]

    async def get_manager(self, user_id: UUID) -> dict:
        user = await self.user_repository.get_user(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')
        if user.role != RoleEnum.MANAGER:
            raise HTTPException(status_code=403, detail='User is not manager')

        return form_manager_response(user)

    async def update_employee(
        self,
        user_id: UUID,
        login: str | Type[Empty] = Empty,
        password: str | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
        surname: str | Type[Empty] = Empty,
        patronymic: str | Type[Empty] = Empty,
        workplace_id: UUID | Type[Empty] = Empty,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
    ):
        worker = await self.user_repository.get_worker(user_id=user_id)
        if not worker:
            raise HTTPException(status_code=404, detail='User not found')
        await self.user_repository.update_worker(worker, workplace_id=workplace_id, grade=grade)

        try:
            await self.user_repository.update_user(worker.user, login=login, password=password, name=name, surname=surname, patronymic=patronymic)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Unable to update user') from e

    async def update_manager(
        self,
        user_id: UUID,
        login: str | Type[Empty] = Empty,
        password: str | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
        surname: str | Type[Empty] = Empty,
        patronymic: str | Type[Empty] = Empty,
    ):
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        if user.role != RoleEnum.MANAGER:
            raise HTTPException(status_code=403, detail='User is not manager')

        try:
            await self.user_repository.update_user(user, login=login, password=password, name=name, surname=surname, patronymic=patronymic)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Unable to update user') from e

    async def delete_employee(self, user_id: UUID):
        worker = await self.user_repository.get_worker(user_id=user_id)
        if not worker:
            raise HTTPException(status_code=404, detail='User not found')

        await self.user_repository.delete_worker(worker)
        await self.user_repository.delete_user(worker.user)

    async def delete_manager(self, user_id: UUID):
        user = await self.user_repository.get_user(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        if user.role != RoleEnum.MANAGER:
            raise HTTPException(status_code=403, detail='User is not manager')

        await self.user_repository.delete_user(user)


def form_employee_response(worker: Worker):
    user: User = worker.user
    workplace_point: Point = worker.workplace.point
    return {
        'id': user.id,
        'workplace': {'id': workplace_point.id, 'address': workplace_point.address, 'city': workplace_point.city},
        'grade': worker.grade,
        'login': user.login,
        'name': user.name,
        'surname': user.surname,
        'patronymic': user.patronymic,
        'role': user.role,
    }


def form_manager_response(manager: User):
    return {'id': manager.id, 'login': manager.login, 'name': manager.name, 'surname': manager.surname, 'patronymic': manager.patronymic, 'role': manager.role}
