import os
from app.config.base_config import BaseConfig
from app.config.dev import DevConfig
from app.config.test import TestConfig
from app.config.prod import ProdConfig


def get_settings() -> BaseConfig:
    env = os.getenv("ENV", "dev")

    if env == "prod":
        return ProdConfig()
    elif env == "test":
        return TestConfig()
    else:
        return DevConfig()


settings = get_settings()
