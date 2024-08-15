from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.database import get_db_session, engine
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app

@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    connection = await engine.connect()
    trans = await connection.begin()
    test_session_factory = async_sessionmaker(connection)
    session = test_session_factory()
    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db_session] = lambda: db_session
    transport = ASGITransport(app=app, client=("127.0.0.1", 8000)) # type: ignore[arg-type]
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

