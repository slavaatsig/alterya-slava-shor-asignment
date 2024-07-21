import pytest
from alterya.service import app, startup_event
from httpx import AsyncClient

from pytest_httpx import HTTPXMock


@pytest.fixture
async def bootstrap():
    yield await startup_event()


@pytest.mark.anyio
@pytest.mark.usefixtures("bootstrap")
async def test_version():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/") as ac:
        response = await ac.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.0.0"}


@pytest.mark.anyio
@pytest.mark.usefixtures("bootstrap")
async def test_tokens_validates():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/v1") as ac:
        response = await ac.get("wallet/%20/chain/1/tokens")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error: Unable to parse data"}


@pytest.mark.anyio
@pytest.mark.usefixtures("bootstrap")
async def test_tokens_moked(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"data": {"items": [{"foo": "bar"}]}})

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/v1/") as ac:
        response = await ac.get("wallet/0x123/chain/1/tokens")
    assert response.status_code == 200
    assert response.json() == {"foo": "bar"}


@pytest.mark.anyio
@pytest.mark.usefixtures("bootstrap")
async def test_balance_moked(httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"data": {"items": [{"quote": 1.0}, {"quote": 2.0}]}})

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/v1/") as ac:
        response = await ac.get("wallet/0x123/chain/1/balance/usd")
    assert response.status_code == 200
    assert response.json() == 3.0
