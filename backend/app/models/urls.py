from pydantic import BaseModel
from uuid import UUID


class UserUrlItem(BaseModel):
    id: UUID
    url: str
    short_code: str


class UserUrlsResponse(BaseModel):
    urls: list[UserUrlItem]