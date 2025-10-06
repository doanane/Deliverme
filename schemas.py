from pydantic import BaseModel, ConfigDict
from typing import Optional


class LoginModel(BaseModel):
    username_or_email: str  # Changed from 'username' to 'username_or_email'
    password: str


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_staff: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access: str
    refresh: str
    token_type: str = "bearer"
    user: UserResponse
