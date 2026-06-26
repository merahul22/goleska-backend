# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "GO LESKA Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URI: str
    REDIS_URI: str
    
    # JWT Security Settings
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    class Config:
        env_file = ".env"

settings = Settings()
