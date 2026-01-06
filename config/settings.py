from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SQL Query Analyzer"
    CACHE_MAX_SIZE: int = 1000
    CACHE_TTL_SECONDS: int = 3600

settings = Settings()