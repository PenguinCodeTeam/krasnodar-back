from typing import Optional

from pydantic import BaseModel

from internal.api.v1.schemas.common import EmployeeUser
from internal.core.types import RoleEnum


class FinishTaskRequest(BaseModel):
    comment: str


class CreateEmployeeUserRequest(EmployeeUser):
    pass


class UpdateUserRequest(BaseModel):
    login: Optional[str]
    password: Optional[str]
    role: Optional[RoleEnum]
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    address: Optional[str]
    grade: Optional[str]
