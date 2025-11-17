import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_token():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        resp = await ac.post('/token', json={'username':'admin','password':'admin123'})
        assert resp.status_code == 200
        data = resp.json()
        assert 'access_token' in data
