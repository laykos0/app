from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    APP_NAME = "App"
    API_TITLE = "App"
    API_DESCRIPTION = "An API for managing an append-only database, which stores articles and their historical " \
                      "versions."

    API_TAGS = [
        {
            "name": "articles",
            "description": "Endpoints related to articles"
        },
        {
            "name": "users",
            "description": "Endpoints related to users"
        }
    ]

    MONGODB_URL: MongoDsn

    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    ORIGINS = [
        "http://localhost:8000",
    ]

    class Config:
        env_file = "./src/.env"


settings = Settings()
