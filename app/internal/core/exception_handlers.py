from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException
from starlette.responses import Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from internal.core.exceptions import UnknownException
from internal.core.logs.helpers import exc_to_log, log_requests


async def unknown_exception_handler(request, exc) -> Response:
    exc_to_log(request)

    exc = UnknownException(cause=exc)

    body = {'errors': [{'code': exc.full_code(), 'name': exc.__class__.__name__, 'message': exc.msg, 'id': str(exc.uuid), 'value': exc.value}]}

    log_requests(route=request.url.path, body=body, log_type='response')

    return JSONResponse(content=body, status_code=500)


async def http_exception_handler(request: Request, exc: HTTPException):
    headers = getattr(exc, 'headers', None)

    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code, headers=headers)


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_to_log(request)
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={'detail': jsonable_encoder(exc.errors())},
    )
