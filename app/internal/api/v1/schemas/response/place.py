from pydantic import BaseModel

from internal.api.v1.schemas.common import IdModel


class CreateWorkplaceResponse(IdModel):
    pass


class GetPlaceResponse(IdModel):
    address: str
    latitude: float
    longitude: float


class GetWorkplacesResponse(BaseModel):
    workplaces: list[GetPlaceResponse]
