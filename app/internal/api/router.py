from fastapi import APIRouter

from internal.api.status import STATUS_ROUTER
from internal.api.v1.router import V1_ROUTER


API_ROUTER = APIRouter()
API_ROUTER.include_router(STATUS_ROUTER)
API_ROUTER.include_router(V1_ROUTER)
