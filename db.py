import beanie
import motor
import motor.motor_asyncio

from api.domain.users import User

MONGODB_URL = 'mongodb://localhost:27017'


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

    await beanie.init_beanie(database=client.db_name, document_models=[User])
