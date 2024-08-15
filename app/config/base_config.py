import enum
from typing import Literal
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field


class LogLevel(str, enum.Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class BaseConfig(BaseSettings):
    ENV: Literal["dev", "test", "prod"] = "dev"
    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    ENABLE_SQL_LOGS: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    WORKERS: int | None = None

    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "postgres"
    PG_PASS: str = "postgres"
    PG_DB: str

    def get_db_url(self, use_db: bool = True) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            host=self.PG_HOST,
            port=self.PG_PORT,
            username=self.PG_USER,
            password=self.PG_PASS,
            path=(self.PG_DB if use_db else None),
        )
