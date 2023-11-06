from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError

from internal.core.types import RoleEnum, WorkerGradeEnum
from internal.repositories.db.models.user import User, Worker
from internal.repositories.db.users import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def create_manager(self, login: str, password: str, name: str, surname: str, patronymic: str) -> UUID:
        try:
            user = await self.repository.add_user(login=login, password=password, name=name, surname=surname, patronymic=patronymic, role=RoleEnum.MANAGER)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='User already exists') from e
        return user.id

    async def create_employee(self, login: str, password: str, name: str, surname: str, patronymic: str, workplace_id: UUID, grade: WorkerGradeEnum) -> UUID:
        try:
            user = await self.repository.add_user(login=login, password=password, name=name, surname=surname, patronymic=patronymic, role=RoleEnum.EMPLOYEE)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='User already exists') from e

        try:
            employee = await self.repository.add_worker(user_id=user.id, workplace_id=workplace_id, grade=grade)
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail='Employee already exists or workplace is invalid') from e

        return employee.user_id

    async def get_employees(self) -> list:
        employees = await self.repository.get_workers()
        return [form_employee_response(worker) for worker in employees]

    async def get_employee(self, user_id: UUID) -> dict:
        worker = await self.repository.get_worker(user_id=user_id)
        if not worker:
            raise HTTPException(status_code=404, detail='Employee not found')

        return form_employee_response(worker)

    async def get_managers(self) -> list:
        users = await self.repository.get_users(role=RoleEnum.MANAGER)
        return [form_manager_response(manager) for manager in users]

    async def get_manager(self, user_id: UUID) -> dict:
        user = await self.repository.get_user(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='Manager not found')
        if user.role != RoleEnum.MANAGER:
            raise HTTPException(status_code=403, detail='User is not manager')

        return form_manager_response(user)


def form_employee_response(worker: Worker):
    user: User = worker.user
    return {
        'id': user.id,
        'address': worker.workplace.point.address,
        'login': user.login,
        'name': user.name,
        'surname': user.surname,
        'patronymic': user.patronymic,
        'role': user.role,
    }


def form_manager_response(manager: User):
    return {'id': manager.id, 'login': manager.login, 'name': manager.name, 'surname': manager.surname, 'patronymic': manager.patronymic, 'role': manager.role}
