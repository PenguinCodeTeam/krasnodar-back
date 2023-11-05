from pydantic import BaseModel

from internal.api.v1.schemas.common import InputDataRow, User


class GetManagerResponse(User):
    pass


class GetInputDataResponse(BaseModel):
    input_data: list[InputDataRow]
