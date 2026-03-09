from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class UserBase(BaseModel):
    email: EmailStr
    role: RoleEnum = RoleEnum.MEMBER


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    password: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool

    model_config = {"from_attributes": True}


class User(UserInDBBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
