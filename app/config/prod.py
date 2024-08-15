from app.config.base_config import BaseConfig, LogLevel


class ProdConfig(BaseConfig):
    PG_DB: str = "fastapi_prod"
    LOG_LEVEL: LogLevel = LogLevel.INFO
    ENABLE_SQL_LOGS: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int | None = 2
