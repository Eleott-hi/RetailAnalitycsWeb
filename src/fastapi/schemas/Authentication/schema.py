

from typing import TypeVar, Optional

from pydantic import BaseModel


T = TypeVar('T')


class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str


class LoginSchema(BaseModel):
    username: str
    password: str


class ForgotPasswordSchema(BaseModel):
    email: str
    new_password: str


class DetailSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None
