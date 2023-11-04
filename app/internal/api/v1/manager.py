from fastapi import APIRouter, Body

from internal.api.v1.schemas.request.manager import CreateManagerRequest, SetInputDataRequest, UpdateManagerRequest


MANAGER_ROUTER = APIRouter(prefix='/manager', tags=['Manager'])


@MANAGER_ROUTER.post('/set_input_data')
async def set_input_data_handler(request_data: SetInputDataRequest = Body()):
    return None


@MANAGER_ROUTER.get('/{user_id}')
async def get_manager_handler(user_id, request_data: CreateManagerRequest):
    return None


@MANAGER_ROUTER.post('/')
async def create_manager_handler(request_data: CreateManagerRequest):
    return None


@MANAGER_ROUTER.patch('/{user_id}')
async def update_manager_handler(user_id: int, request_data: UpdateManagerRequest):
    return None
