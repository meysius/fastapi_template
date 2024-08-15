from typing import AsyncGenerator
from sqlalchemy import text, MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.config import settings

engine = create_async_engine(str(settings.get_db_url()))
session_factory = async_sessionmaker(engine)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session = session_factory()
    try:
        yield session
    finally:
        await session.commit()
        await session.close()


admin_engine = create_async_engine(
    str(settings.get_db_url(use_db=False)), isolation_level="AUTOCOMMIT"
)


async def database_exists() -> bool:
    async with admin_engine.connect() as conn:
        database_existance = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{settings.PG_DB}'"),
        )
        return database_existance.scalar() == 1


async def create_database() -> None:
    db_exists = await database_exists()
    if db_exists:
        print(f"Database {settings.PG_DB} already exists.")
    else:
        print(f"Creating database {settings.PG_DB}")
        async with admin_engine.connect() as conn:
            await conn.execute(
                text(f'CREATE DATABASE "{settings.PG_DB}" ENCODING "utf8"'),
            )


async def drop_database() -> None:
    db_exists = await database_exists()
    if not db_exists:
        print(f"Database {settings.PG_DB} does not exist.")
    else:
        print(f"Dropping database {settings.PG_DB}")
        async with admin_engine.connect() as conn:
            await conn.execute(
                text(f'DROP DATABASE "{settings.PG_DB}"'),
            )


metadata = MetaData()
