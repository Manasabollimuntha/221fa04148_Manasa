# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_uri: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    openai_api_key: str | None = None
    email_user: str | None = None
    email_pass: str | None = None
    smtp_server: str | None = None
    smtp_port: int | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
