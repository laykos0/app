from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "App"


settings = Settings()

api_title = "App"
api_description = "An API for managing an append-only database, which stores articles and their historical versions."

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
