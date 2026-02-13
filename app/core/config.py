"""Application configuration settings"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and environment variables"""
    
    # Project metadata
    PROJECT_NAME: str = "Universal Notifier API"
    VERSION: str = "0.1.0"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # MongoDB Configuration
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB_NAME: str = "notifier_db"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
