import pytest
from alterya.service import app
from httpx import AsyncClient


@pytest.mark.anyio
async def test_version():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        response = await ac.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.0"}
