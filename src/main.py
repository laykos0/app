from datetime import timedelta
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware

from src.api import routers
from src.api.routers.exception_handlers import handle_404_not_found
from src.core.mongo import init_db
from src.core.settings import settings
from src.domain.users import User
from src.infrastructure.exceptions import CustomNotFoundException, UserNotFoundException
from src.infrastructure.services.auth import authenticate_user, Token, create_access_token, \
    get_current_user

app = FastAPI(title=settings.api_title,
              description=settings.api_description,
              openapi_tags=settings.api_tags)
app.include_router(routers.router)


@app.on_event('startup')
async def connect():
    await init_db()


@app.get("/")
async def root():
    return {
        "app_name": settings.app_name,
    }


@app.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise UserNotFoundException(PydanticObjectId(form_data.username))
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(CustomNotFoundException, handle_404_not_found)
