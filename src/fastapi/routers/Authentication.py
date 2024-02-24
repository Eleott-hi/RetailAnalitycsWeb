from fastapi import APIRouter, Form
from services.Authentication import AuthService
from schemas.Authentication.schema import (
    RegisterSchema,
    LoginSchema,
    ForgotPasswordSchema,
    ResponseSchema,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(request_body: RegisterSchema):
    await AuthService.register(request_body)
    return "User successfully registered!"


@router.post("/login")
async def login(requset_body: LoginSchema):
    token = await AuthService.login(requset_body)
    return {
        "detail": "Successfully login",
        "result": {"token_type": "Bearer", "access_token": token},
    }


@router.post("/forgot-password")
async def forgot_password(request_body: ForgotPasswordSchema):
    await AuthService.forgot_password(request_body)
    return "Password successfully updated!"
