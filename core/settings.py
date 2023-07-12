from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    app_name: str = "App"
    mongodb_url: MongoDsn
    api_title = "App"
    api_description = "An API for managing an append-only database, which stores articles and their historical " \
                      "versions."

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
        env_file = ".env"


settings = Settings()
