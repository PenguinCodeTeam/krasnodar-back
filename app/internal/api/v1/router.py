from fastapi import APIRouter

from internal.api.v1.authentication import AUTH_ROUTER
from internal.api.v1.employee import EMPLOYEE_ROUTER
from internal.api.v1.manager import MANAGER_ROUTER
from internal.api.v1.tasks import TASKS_ROUTER


V1_ROUTER = APIRouter(prefix='/v1')
V1_ROUTER.include_router(AUTH_ROUTER)
V1_ROUTER.include_router(EMPLOYEE_ROUTER)
V1_ROUTER.include_router(MANAGER_ROUTER)
V1_ROUTER.include_router(TASKS_ROUTER)
