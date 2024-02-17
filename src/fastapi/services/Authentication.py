from fastapi import HTTPException, status

from passlib.context import CryptContext
import repositories.CRUD as CRUD
import database.Models as DBModels
from services.JWT import JWTService
from schemas.Authentication.schema import RegisterSchema, LoginSchema, ForgotPasswordSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def register(register: RegisterSchema):

        _user = CRUD.one(DBModels.User,
                         CRUD.Operations(filters=[DBModels.User.username == register.username]))

        if _user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists!"
            )

        _email = CRUD.one(DBModels.User,
                          CRUD.Operations(filters=[DBModels.User.email == register.email]))

        if _email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists!"
            )

        _role = CRUD.one(DBModels.Role,
                         CRUD.Operations(filters=[DBModels.Role.name == "user"]))

        CRUD.create(DBModels.User, **{
            "username": register.username,
            "password": pwd_context.hash(register.password),
            "email": register.email,
            "role_id": _role.id
        })

    @staticmethod
    async def login(login: LoginSchema):
        _user = CRUD.one(DBModels.User,
                         CRUD.Operations(filters=[DBModels.User.username == login.username]))

        if _user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Username not found !")

        if not pwd_context.verify(login.password, _user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password !")

        return JWTService.generate_token(data={"username": _user.username})

    @staticmethod
    async def forgot_password(forgot_password: ForgotPasswordSchema):
        _user = CRUD.one(DBModels.User,
                         CRUD.Operations(filters=[DBModels.User.email == forgot_password.email]))

        if _user is None:
            raise HTTPException(status_code=404, detail="Email not found !")

        _user.password = pwd_context.hash(forgot_password.new_password)

        CRUD.update(DBModels.User,
                    CRUD.Operations(filters=[DBModels.User.id == _user.id]),
                    **_user.dict())
