from pydantic import BaseModel


class CreateWorkplaceRequest(BaseModel):
    address: str
