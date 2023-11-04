from pydantic import BaseModel

from internal.core.types import RoleEnum


class EmployeeUser(BaseModel):
    role: RoleEnum = RoleEnum.EMPLOYEE
    address: str
    grade: str


class User(BaseModel):
    login: str
    password: str
    role: RoleEnum
    name: str
    surname: str
    patronymic: str
