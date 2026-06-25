# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "GO LESKA Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URI: str
    REDIS_URI: str

    class Config:
        env_file = ".env"

settings = Settings()
