from app.config.base_config import BaseConfig


class DevConfig(BaseConfig):
    PG_DB: str = "fastapi_dev"
