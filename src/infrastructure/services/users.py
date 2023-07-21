from beanie import PydanticObjectId
from dataclass_mapper import map_to

from src.domain.users import (
    UserInDB,
    User
)
from src.infrastructure.dto import (
    UserCreateDTO,
    UserUpdateDTO
)
from src.infrastructure.exceptions import UserNotFoundException
from src.infrastructure.repositories.users import (
    insert,
    find,
    find_all,
    update,
    delete
)
from src.infrastructure.services.auth import get_password_hash


async def post(user_create_dto: UserCreateDTO):
    hashed_password = get_password_hash(user_create_dto.password)
    user = map_to(user_create_dto, User)
    user_in_db = map_to(user, UserInDB, extra={"hashed_password": hashed_password})
    await insert(user_in_db)


async def get(user_id: PydanticObjectId):
    if user := await find(user_id):
        return map_to(user, User)
    raise UserNotFoundException(user_id)


async def get_all():
    users_in_db = await find_all()
    users = [map_to(user_in_db, User) for user_in_db in users_in_db]
    return users


async def put(user_id: PydanticObjectId, user_update_dto: UserUpdateDTO):
    if user := await find(user_id):
        hashed_password = get_password_hash(user_update_dto.password)
        user_update = map_to(user_update_dto, User)
        user.patch(user_update.name, user_update.role, hashed_password)
        return await update(user)
    raise UserNotFoundException(user_id)


async def remove(user_id: PydanticObjectId):
    if user := await find(user_id):
        return await delete(user)
    raise UserNotFoundException(user_id)
