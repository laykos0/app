from beanie import PydanticObjectId

from src.domain.users import UserInDB


async def insert(user: UserInDB):
    return await user.insert()


async def find(user_id: PydanticObjectId):
    return await UserInDB.get(user_id)


async def find_all():
    return await UserInDB.find_all().to_list()


async def update(user: UserInDB):
    return await user.save()


async def delete(user: UserInDB):
    await user.delete()
