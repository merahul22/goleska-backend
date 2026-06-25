# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "GO LESKA Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URI: str = "postgresql+asyncpg://user:password@localhost:5433/goleska"
    REDIS_URI: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
