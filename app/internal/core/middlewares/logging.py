import json
import typing
from json import JSONDecodeError

from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import StreamingResponse

from internal.core.logs.helpers import log_requests


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    async def set_body(request: Request, body: bytes):
        async def receive():
            return {'type': 'http.request', 'body': body}

        request._receive = receive

    @staticmethod
    def validate_body(body: typing.Any) -> typing.Any:
        if not body:
            return None
        try:
            return json.loads(body)
        except JSONDecodeError:
            return body

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Чтение и сохранение тела запроса
        req_body = await request.body()
        await self.set_body(request, req_body)

        # Получение пути запроса и его параметров
        route = request.url.path
        req_query = dict(request.query_params)

        # Логирование запроса
        log_requests(route=route, body=self.validate_body(req_body), log_type='request', query=req_query)

        # Обработка запроса и получение ответа
        response = typing.cast(StreamingResponse, await call_next(request))

        # Чтение тела ответа
        res_body: bytes = b''
        async for chunk in response.body_iterator:
            res_body += chunk if isinstance(chunk, bytes) else chunk.encode()

        # Логирование ответа
        log_requests(route=route, body=self.validate_body(res_body), log_type='response')

        # Формирование и возвращение ответа
        return Response(content=res_body, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
