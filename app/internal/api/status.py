from fastapi.responses import PlainTextResponse
from fastapi import APIRouter


STATUS_ROUTER = APIRouter()


@STATUS_ROUTER.get('/status')
async def status_handler():
    return {
        'status': 'ok'
    }


@STATUS_ROUTER.get('/ping', response_class=PlainTextResponse)
async def pingpong_handler():
    return 'PONG'
