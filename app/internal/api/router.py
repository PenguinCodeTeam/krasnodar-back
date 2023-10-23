from fastapi import APIRouter

from internal.api.status import STATUS_ROUTER


API_ROUTER = APIRouter(prefix='/api')
API_ROUTER.include_router(STATUS_ROUTER)
