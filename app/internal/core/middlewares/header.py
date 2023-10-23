from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from internal.core.requests import generate_request_id, request_id_var


class AddHeaderMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def set_request_id(request: Request):
        if request_id := request.headers.get('X-Request-ID'):
            request_id_var.set(request_id)
        else:
            request_id_var.set(generate_request_id())

    @staticmethod
    def add_no_cache_header_to_get(request: Request, response: Response):
        if request.method == 'GET':
            response.headers['Cache-Control'] = 'No-Cache'
        return response

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        self.set_request_id(request)
        response = await call_next(request)
        return self.add_no_cache_header_to_get(request, response)
