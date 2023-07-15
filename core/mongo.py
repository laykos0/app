import beanie
import motor
import motor.motor_asyncio

from domain.articles import Article
from domain.users import User
from core.settings import settings


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)

    await beanie.init_beanie(database=client.db_name, document_models=[User, Article])
