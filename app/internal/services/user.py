from uuid import UUID

from fastapi.exceptions import HTTPException

from internal.core.types import RoleEnum, WorkerGradeEnum
from internal.repositories.db.users import UserRepository
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create_manager(self, login: str, password: str, name: str, surname: str, patronymic: str) -> UUID:
        try:
            user = await self.repository.add_user(login, password, name, surname, patronymic, RoleEnum.MANAGER)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='User already exists') from e
        return user.id

    async def create_employee(self, login: str, password: str, name: str, surname: str, patronymic: str, workplace_id: UUID, grade: WorkerGradeEnum) -> UUID:
        try:
            user = await self.repository.add_user(login, password, name, surname, patronymic, RoleEnum.EMPLOYEE)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='User already exists') from e

        try:
            employee = await self.repository.add_worker(user.id, workplace_id, grade)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Employee already exists') from e

        return employee.user_id

    async def get_employees(self) -> list:
        employees = await self.repository.get_workers()
        data = []
        for worker in employees:
            user = worker.user
            data.append(
                {
                    'id': user.id,
                    'address': worker.workplace.point.address,
                    'login': user.login,
                    'name': user.name,
                    'surname': user.surname,
                    'patronymic': user.patronymic,
                    'role': user.role,
                }
            )
        return data

    async def get_employee(self, user_id: UUID) -> dict:
        worker = await self.repository.get_worker(user_id=user_id)
        if not worker:
            raise HTTPException(status_code=404, detail='Employee not found')

        user = worker.user

        result = {
            'id': user_id,
            'address': worker.workplace.point.address,
            'login': user.login,
            'name': user.name,
            'surname': user.surname,
            'patronymic': user.patronymic,
            'role': user.role,
        }
        return result

    async def get_managers(self) -> list:
        users = await self.repository.get_users(role=RoleEnum.MANAGER)
        result = []
        for user in users:
            result.append({'id': user.id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'patronymic': user.patronymic, 'role': user.role})
        return result

    async def get_manager(self, user_id: UUID) -> dict:
        user = await self.repository.get_user(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='Manager not found')
        if user.role != RoleEnum.MANAGER:
            raise HTTPException(status_code=403, detail='User is not manager')

        result = {'id': user_id, 'login': user.login, 'name': user.name, 'surname': user.surname, 'patronymic': user.patronymic, 'role': user.role}
        return result
