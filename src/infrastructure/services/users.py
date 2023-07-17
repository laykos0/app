from beanie import PydanticObjectId

from src.domain.users import UserCreateDTO, UserUpdateDTO
from src.infrastructure.exceptions import UserNotFoundException
from src.infrastructure.repositories.users import insert, find, find_all, update, delete


async def post(user_create_dto: UserCreateDTO):
    await insert(user_create_dto.to_document())


async def get(user_id: PydanticObjectId):
    if user := await find(user_id):
        return user
    raise UserNotFoundException(user_id)


async def get_all():
    return await find_all()


async def put(user_id: PydanticObjectId, user_update_dto: UserUpdateDTO):
    user = await get(user_id)
    user_update = user_update_dto.to_document()
    user.update(user_update.name, user_update.role)
    await update(user)


async def remove(user_id: PydanticObjectId):
    user = await get(user_id)
    await delete(user)
