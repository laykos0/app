from datetime import timedelta, datetime
from typing import Annotated

from beanie import PydanticObjectId
from bson.errors import InvalidId
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.settings import settings
from src.domain.role import Role
from src.domain.token import TokenData
from src.domain.users import UserInDB
from src.infrastructure.exceptions import (
    InvalidCredentialsException,
    InsufficientPermissionException
)
from src.infrastructure.repositories.users import find

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    try:
        if user := await find(PydanticObjectId(username)):
            return user
    except InvalidId:
        raise InvalidCredentialsException


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if verify_password(password, user.hashed_password):
        return user
    raise InvalidCredentialsException


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise InvalidCredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise InvalidCredentialsException
    user = await get_user(username=token_data.username)
    return user


async def get_current_user_id(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return current_user.id


async def is_admin(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    if current_user.role != Role.admin:
        raise InsufficientPermissionException(current_user.id, Role.admin)
