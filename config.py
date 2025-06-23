from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Настройки сервера
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Настройки базы данных
    database_url: Optional[str] = None
    
    # Настройки CORS
    cors_origins: List[str] = ["*"]
    
    # Настройки безопасности
    admin_token: Optional[str] = None
    
    # Настройки Telegram
    bot_token: Optional[str] = None  # Для верификации запросов от бота
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Settings() 