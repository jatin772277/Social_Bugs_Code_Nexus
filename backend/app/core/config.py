from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    database_url:str=os.getenv("DATABASE_URL","sqlite:///./codenexus.db")
    secret_key:str=os.getenv("SECRET_KEY","codenexus-secret-key-32chars-long")
    algorithm:str="HS256"
    access_token_expire_minutes:int=1440
    gemini_api_key:str=os.getenv("GEMINI_API_KEY","")
    gemini_model:str="gemini-3.8-flash"
    upload_dir:str="uploads"
    max_file_size_mb:int=20
    class Config:
        env_file=".env"

@lru_cache()
def get_settings():
    return Settings()
