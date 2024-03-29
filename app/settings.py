import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    ENVIRONMENT: str = "prod"
    POSTGRESQL_CONNECTION_URL: str
    POSTGRESQL_CONNECTION_URL_TEST: str
    ACCESS_TOKEN_SECRET_KEY: str
    REFRESH_TOKEN_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    RESEND_API_KEY: str
    ACTIVATION_TOKEN_EXPIRE_MINUTES: int


settings = Settings()


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
