from typing import Optional

from pydantic import BaseModel, EmailStr


class RegistrationBody(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginBody(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: Optional[str] = None
    message: str
