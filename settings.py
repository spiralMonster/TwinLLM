from loguru import logger
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    #Mongodb Configs:
    MONGODB_DATABASE_HOST: str ="mongodb://admin:password@mongodb:27017/admin?authSource=admin"
    MONGODB_DATABASE_NAME: str ="llm_twin_data"

