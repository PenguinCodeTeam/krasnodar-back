from fastapi import APIRouter, Body, Depends, Response

from internal.api.v1.schemas.request import LoginRequest
from internal.api.v1.schemas.response import CheckAuthResponse
from internal.core.dependencies import EmployeeAuthorize
from internal.services.authentication.authentication import AuthenticationService


AUTH_ROUTER = APIRouter(tags=['Authentication'])


@AUTH_ROUTER.post('/login')
async def login_handler(request_data: LoginRequest = Body(), service: AuthenticationService = Depends()):
    await service.login_service(**request_data.model_dump())
    return Response(status_code=200)


@AUTH_ROUTER.get('/check_auth', dependencies=[Depends(EmployeeAuthorize())])
async def check_auth_handler() -> CheckAuthResponse:
    return CheckAuthResponse()
