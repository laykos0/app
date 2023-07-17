from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    app_name = "App"
    api_title = "App"
    api_description = "An API for managing an append-only database, which stores articles and their historical " \
                      "versions."
    MONGODB_URL: MongoDsn

    api_tags = [
        {
            "name": "articles",
            "description": "Endpoints related to articles"
        },
        {
            "name": "users",
            "description": "Endpoints related to users"
        }
    ]

    class Config:
        env_file = "./src/.env"


settings = Settings()
