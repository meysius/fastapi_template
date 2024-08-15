import pytest
from fastapi import status
from httpx import AsyncClient

@pytest.mark.anyio
async def test_creation(client: AsyncClient) -> None:
    response = await client.post("/users", json={"email": "test@example.com", "password": "test"})
    assert response.status_code == status.HTTP_200_OK
