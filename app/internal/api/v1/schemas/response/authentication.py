from pydantic import BaseModel


class CheckAuthResponse(BaseModel):
    status: str = 'OK'
