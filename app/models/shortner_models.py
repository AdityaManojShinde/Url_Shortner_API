from pydantic import BaseModel, HttpUrl, Field, field_validator
from urllib.parse import urlparse
from uuid import UUID

class ShortnerReq(BaseModel):
    # inforce 2000 char limit
    url: str = Field(...,max_length=2000)

    @field_validator("url")
    @classmethod
    def validate_url(cls, url):
        """Validate Url"""
        parsed = urlparse(url)
        if not parsed.scheme or parsed.scheme not in ("http", "https"):
            raise ValueError("URL scheme must be http or https.")
        if not parsed.netloc or "." not in parsed.netloc:
            raise ValueError("URL must include a valid domain.")  
        return url

class ShortnerRes(BaseModel):
    id: UUID
    url: HttpUrl
    short_url: HttpUrl
    short_code: str