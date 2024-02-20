
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt

from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES


class JWTService:
    @staticmethod
    def generate_token(data: dict, expires_delta: int = JWT_ACCESS_TOKEN_EXPIRE_MINUTES):
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)

        data = {**data, 'exp': expire}

        encoded = JWTService.encode(data)
        return encoded

    @staticmethod
    def decode(token: str) -> Optional[dict]:
        try:
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
            return data

        except JWTError as e:
            raise HTTPException(status_code=401,
                                detail=f"Invalid authentication credentials: {e}")

    @staticmethod
    def encode(data: Dict) -> str:
        try:
            token = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            return token

        except JWTError as e:
            raise HTTPException(status_code=401,
                                detail=f"Invalid data: {e}")


class JWTBearer():
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    async def __call__(self, token: str = Depends(oauth2_scheme)):

        """
        Dependency function to verify the token.
        """
        print("TOKEN:", token)
        print("EXTRACT TOKEN:", JWTService.decode(token))
        return token
