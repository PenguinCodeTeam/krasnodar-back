from fastapi import APIRouter

from internal.api.v1.authentication import AUTH_ROUTER


V1_ROUTER = APIRouter(prefix='/v1')
V1_ROUTER.include_router(AUTH_ROUTER)
