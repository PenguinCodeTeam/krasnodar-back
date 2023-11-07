from pydantic import BaseModel

from internal.api.v1.schemas.common import IdModel, Point


class CreateWorkplaceResponse(IdModel):
    pass


class GetPlaceResponse(Point):
    pass


class GetWorkplacesResponse(BaseModel):
    workplaces: list[GetPlaceResponse]
