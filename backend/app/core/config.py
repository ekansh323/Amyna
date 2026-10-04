from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Aegis"
    DATABASE_URL: str = "sqlite:///./aegis.db"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    API_PREFIX: str = "/api/v1"
    
    # JWT Settings
    JWT_SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # In production, this should be overriden via .env
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days

    class Config:
        env_file = ".env"

settings = Settings()
