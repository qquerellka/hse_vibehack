"""Настройки приложения."""
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Основные настройки
    APP_NAME: str = "Vaiboton API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Настройки базы данных
    DATABASE_URL: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "vaiboton"
    
    # Настройки безопасности
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]

    # OpenRouter (LLM agents)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # Tavily (web search for WriterAgent)
    TAVILY_API_KEY: str = ""

    # File storage
    DOWNLOADS_DIR: str = "./downloads"
    EXTRACTED_IMAGES_DIR: str = "./extracted_images"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

