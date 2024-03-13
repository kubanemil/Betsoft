import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import app

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


async def test_create_bet_success(client):
    response = await client.post("/bet", json={"event_id": 1, "amount": 10.5123})
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == 1
    assert data["amount"] == 10.51
    assert data["has_won"] is None
    assert "id" in data
    assert "created_at" in data


async def test_create_bet_invalid_amount(client):
    response = await client.post("/bet", json={"event_id": 1, "amount": -5})
    assert response.status_code == 422


async def test_get_bets(client):
    response = await client.get("/bets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "id" in data[0]
    assert "event_id" in data[0]


async def test_update_event_success(client):
    response = await client.put("/events/1", params={"has_won": True})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "id" in data[0]
    assert "event_id" in data[0]


async def test_update_event_not_found(client):
    response = await client.put("/events/999", params={"has_won": True})
    assert response.status_code == 404
