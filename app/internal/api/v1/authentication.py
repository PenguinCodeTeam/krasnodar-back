from fastapi import APIRouter, Body, Depends

from internal.api.v1.schemas.request import LoginRequest
from internal.api.v1.schemas.response.authentication import CheckAuthResponse, LoginResponse
from internal.core.dependencies import EmployeeAuthorize
from internal.services.authentication.authentication import AuthenticationService


AUTH_ROUTER = APIRouter(prefix='/auth', tags=['Authentication'])


@AUTH_ROUTER.post('/login')
async def login_handler(request_data: LoginRequest = Body(), service: AuthenticationService = Depends()) -> LoginResponse:
    data = await service.login_service(**request_data.model_dump())
    return LoginResponse(**data)


@AUTH_ROUTER.get('/logout')
async def logout_handler() -> None:
    return None


@AUTH_ROUTER.get('/check_auth', dependencies=[Depends(EmployeeAuthorize())])
async def check_auth_handler() -> CheckAuthResponse:
    return CheckAuthResponse()
