import uuid
from typing import Type

from internal.core.types import Empty, RoleEnum, WorkerGradeEnum
from internal.core.utils import hash_password
from internal.repositories.db.base import DatabaseRepository
from internal.repositories.db.models import User, Worker
from sqlalchemy import select


class UserRepository(DatabaseRepository):
    async def get_user(
        self,
        user_id: uuid.UUID | Type[Empty] = Empty,
        login: str | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
        surname: str | Type[Empty] = Empty,
        patronymic: str | Type[Empty] = Empty,
        role: RoleEnum | Type[Empty] = Empty,
    ) -> User | None:
        filters = []
        if user_id is not Empty:
            filters.append(User.id == user_id)
        if login is not Empty:
            filters.append(User.login == login)
        if name is not Empty:
            filters.append(User.name == name)
        if surname is not Empty:
            filters.append(User.surname == surname)
        if patronymic is not Empty:
            filters.append(User.patronymic == patronymic)
        if role is not Empty:
            filters.append(User.role == role)

        query = select(User).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalar_one_or_none()

    async def get_users(self, role: RoleEnum | Type[Empty] = Empty) -> tuple[User]:
        filters = []
        if role is not Empty:
            filters.append(User.role == role)

        query = select(User).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.scalars().all()

    async def add_user(
        self,
        login: str,
        password: str,
        name: str,
        surname: str,
        patronymic: str,
        role: RoleEnum,
    ) -> User:
        user = User(login=login, password=hash_password(password), name=name, surname=surname, patronymic=patronymic, role=role)
        async with self.transaction() as session:
            session.add(user)

        return user

    async def update_user(
        self,
        user: User,
        login: str | Type[Empty] = Empty,
        password: str | Type[Empty] = Empty,
        name: str | Type[Empty] = Empty,
        surname: str | Type[Empty] = Empty,
        patronymic: str | Type[Empty] = Empty,
        role: RoleEnum | Type[Empty] = Empty,
    ) -> User:
        if login is not Empty:
            user.login = login
        if password is not Empty:
            user.password = hash_password(password)
        if name is not Empty:
            user.name = name
        if surname is not Empty:
            user.surname = surname
        if patronymic is not Empty:
            user.patronymic = patronymic
        if role is not Empty:
            user.role = role
        async with self.transaction() as session:
            session.add(user)

        return user

    async def delete_user(self, user: User) -> User:
        async with self.transaction() as session:
            session.delete(user)

        return user

    async def get_worker(self, user_id: uuid.UUID) -> Worker | None:
        query = select(Worker).where(Worker.user_id == user_id)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalar_one_or_none()

    async def get_workers(
        self,
        workplace_id: uuid.UUID | Type[Empty] = Empty,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
    ) -> tuple[Worker]:
        filters = []
        if workplace_id is not Empty:
            filters.append(Worker.workplace_id == workplace_id)
        if grade is not Empty:
            filters.append(Worker.grade == grade)

        query = select(Worker).where(*filters)
        async with self.transaction() as session:
            res = await session.execute(query)

        return res.unique().scalars().all()

    async def add_worker(self, user_id: uuid.UUID, workplace_id: uuid.UUID, grade: WorkerGradeEnum) -> Worker:
        worker = Worker(user_id=user_id, workplace_id=workplace_id, grade=grade)
        async with self.transaction() as session:
            session.add(worker)

        return worker

    async def update_worker(
        self,
        worker: Worker,
        workplace_id: uuid.UUID | Type[Empty] = Empty,
        grade: WorkerGradeEnum | Type[Empty] = Empty,
    ) -> Worker:
        if workplace_id is not Empty:
            worker.workplace_id = workplace_id
        if grade is not Empty:
            worker.grade = grade

        async with self.transaction() as session:
            session.add(worker)

        return worker

    async def delete_worker(self, worker: Worker) -> Worker:
        async with self.transaction() as session:
            session.delete(worker)

        return worker
