import uvicorn
from fastapi import FastAPI
from typing import AsyncGenerator
from fastapi import FastAPI
from app.database import engine
from app.routers.user_router import router as user_router
from contextlib import asynccontextmanager
from app.config import settings
import logging
import coloredlogs  # type: ignore[import-untyped]


def setup_logging() -> None:
    log_format = "%(asctime)s [%(levelname)s] %(name)s %(message)s"
    loggers = {
        "": {
            "level": settings.LOG_LEVEL.value,
            "handlers": ["default"],
            "propagate": False,
        },
        "uvicorn": {
            "level": settings.LOG_LEVEL.value,
            "handlers": ["default"],
        },
        "sqlalchemy.engine": {
            "level": "INFO" if settings.ENABLE_SQL_LOGS else "WARNING",
            "handlers": ["default"],
            "propagate": False,
        },
        "sqlalchemy.pool": {
            "level": "INFO" if settings.ENABLE_SQL_LOGS else "WARNING",
            "handlers": ["default"],
            "propagate": False,
        },
    }
    logging_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {"format": log_format},
        },
        "handlers": {
            "default": {
                "level": settings.LOG_LEVEL.value,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": loggers,
    }

    logging.config.dictConfig(logging_config)

    if settings.ENV == "dev":
        configured_loggers = loggers.keys()
        for name in configured_loggers:
            logger = logging.getLogger(name)
            level_name = logging.getLevelName(logger.level)
            coloredlogs.install(
                logger=logger,
                fmt=log_format,
                field_styles={
                    "asctime": {"color": "green"},
                    "hostname": {"color": "blue"},
                    "levelname": {"color": "black", "bold": True},
                    "name": {"color": "magenta"},
                    "programname": {"color": "cyan"},
                    "username": {"color": "yellow"},
                },
                level=level_name,
            )


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:  # pragma: no cover
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


def main() -> None:
    uvicorn.run(
        root_path="",
        app="app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
    )


if __name__ == "__main__":
    main()
