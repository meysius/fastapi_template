from app.config.base_config import BaseConfig


class TestConfig(BaseConfig):
    PG_DB: str = "fastapi_test"
