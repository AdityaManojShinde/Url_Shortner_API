from pydantic import BaseModel
from pydantic import Field, EmailStr
from datetime import datetime
from uuid import UUID

class SignUpUserReq(BaseModel):
    email: EmailStr = Field(examples=["aditya@gmail.com"])
    password: str = Field(min_length=6,examples=["123456"])

class SignUpUserRes(BaseModel):
    email: EmailStr
    msg: str = Field(default="signup successfull")


class LoginUserReq(BaseModel):
    email: EmailStr = Field(examples=["aditya@gmail.com"])
    password: str = Field(min_length=6,examples=["123456"])


class LoginUserRes(BaseModel):
    access_token: str
    token_type: str

class MeResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime