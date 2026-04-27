from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Switch Admin Platform"
    APP_ENV: str = "development"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 120
    ENCRYPTION_KEY: str
    SSH_TIMEOUT: int = 10
    MONITOR_INTERVAL_SECONDS: int = 60
    CORS_ORIGINS: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> List[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

    class Config:
        env_file = ".env"

settings = Settings()
