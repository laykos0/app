from beanie import PydanticObjectId

from src.domain.users import UserCreateDTO, UserUpdateDTO, UserInDB
from src.infrastructure.exceptions import UserNotFoundException
from src.infrastructure.repositories.users import insert, find, find_all, update, delete
from src.infrastructure.services.auth import get_password_hash


async def post(user_create_dto: UserCreateDTO, password: str):
    user = user_create_dto.to_document()
    user = UserInDB(name=user.name, role=user.role,
                    hashed_password=get_password_hash(password))
    await insert(user)


async def get(user_id: PydanticObjectId):
    if user := await find(user_id):
        return user.to_user()
    raise UserNotFoundException(user_id)


async def get_all():
    users_in_db = await find_all()
    users = [user_in_db.to_user() for user_in_db in users_in_db]
    return users


async def put(user_id: PydanticObjectId, user_update_dto: UserUpdateDTO):
    if user := await find(user_id):
        user_update = user_update_dto.to_document()
        user.patch(user_update.name, user_update.role)
        return await update(user)
    raise UserNotFoundException(user_id)


async def remove(user_id: PydanticObjectId):
    if user := await find(user_id):
        await delete(user)
    raise UserNotFoundException(user_id)
