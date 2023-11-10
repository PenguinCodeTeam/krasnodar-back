from pydantic import BaseModel

from internal.api.v1.schemas.common import DestinationDataRowRequest


class SetInputDataRequest(BaseModel):
    city: str = 'Краснодар'
    destinations: list[DestinationDataRowRequest]


class CreateManagerRequest(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    patronymic: str


class UpdateManagerRequest(BaseModel):
    login: str = None
    password: str = None
    name: str = None
    surname: str = None
    patronymic: str = None
