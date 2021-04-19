import os
import secrets
from typing import Any, List

from pydantic import AnyUrl, BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):

    SECRET_KEY:str = secrets.token_urlsafe(32)
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    DATABASE_URI:str = os.getenv('DATABASE_URI')

    ORIGINS: List[Any] = [
            "http://localhost"
        ]
    ALLOWED_HOSTS: List[Any] = [
            "http://localhost"
        ]

    class Config:
        case_sensitive:bool = True
        env_file:str = ".env"

settings = Settings()