"""
Application configuration using Pydantic settings.
This handles environment variables and app configuration.
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # WhatsApp Cloud API Configuration
    whatsapp_access_token: str
    whatsapp_phone_number_id: str
    webhook_verify_token: str
    
    # Database Configuration
    database_url: str = "sqlite:///./interview_bot.db"
    
    # OpenAI Configuration (for response analysis)
    openai_api_key: Optional[str] = None
    
    # Application Settings
    debug: bool = False
    daily_question_hour: int = 9  # Send questions at 9 AM
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()