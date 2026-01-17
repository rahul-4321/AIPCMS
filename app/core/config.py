import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):

    PROJECT_NAME: str = "AI-Powered Content Moderation System"

    #Database
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")

    @property
    def DATABASE_URL(self) -> str:
        url = os.getenv("DATABASE_URL")
        if url:
            return url
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    #Moderation
    MODERATION_THRESHOLD: float = float(os.getenv("MODERATION_THRESHOLD", "0.7"))
    NLP_MODEL_NAME: str = os.getenv("NLP_MODEL_NAME")
    VISION_MODEL_NAME: str = os.getenv("VISION_MODEL_NAME")
    MAX_TOXIC_CONTENT: int = int(os.getenv("MAX_TOXIC_CONTENT", "3"))

settings = Settings()