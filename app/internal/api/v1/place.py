from uuid import UUID

from fastapi import APIRouter, Depends

from internal.api.v1.schemas.request.place import CreateWorkplaceRequest
from internal.api.v1.schemas.response.place import CreateWorkplaceResponse, GetPlaceResponse, GetWorkplacesResponse
from internal.services.point import PointService


PLACE_ROUTER = APIRouter(prefix='/place', tags=['Place'])


@PLACE_ROUTER.post('/workplace', tags=['Working'])
async def create_workplace_handler(request_data: CreateWorkplaceRequest, service: PointService = Depends()) -> CreateWorkplaceResponse:
    """Создание рабочей точки. Вероятно временный сервис для удобства разработки"""
    workplace_id = await service.add_workplace(**request_data.model_dump())
    return CreateWorkplaceResponse(id=workplace_id)


@PLACE_ROUTER.get('/workplace', tags=['Working'])
async def get_workplaces_handler(service: PointService = Depends()) -> GetWorkplacesResponse:
    data = await service.get_workplaces()
    return GetWorkplacesResponse(workplaces=data)


@PLACE_ROUTER.get('/workplace/{point_id}', tags=['Working'])
async def get_workplace_handler(point_id: UUID, service: PointService = Depends()) -> GetPlaceResponse:
    data = await service.get_workplace(point_id)
    return GetPlaceResponse.model_validate(data)
