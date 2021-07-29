import asyncio
from typing import Generator

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.pylint import MODELS
from tortoise.contrib.test import finalizer, initializer

from backend.app.users.models import User
from backend.app.users.utils import create_password_hash
from backend.main import app


@pytest.fixture(scope='module', autouse=True)
def client() -> Generator:
    initializer(modules=MODELS)
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope='module')
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture(scope='module')
def admin_user() -> dict:
    return {
        'username': 'admin',
        'password': 'secret',
        'is_admin': True
    }


@pytest.fixture(scope='module')
def default_user() -> dict:
    return {
        'username': 'default',
        'password': 'secret',
        'is_admin': False
    }


def get_headers(client: TestClient, user_data: dict, event_loop: asyncio.AbstractEventLoop):
    """Setups user in test database, returns auth headers for this user"""

    async def create_admin_user():
        password = await create_password_hash(user_data.get('password'))
        return await User.create(**user_data, password_hash=password)

    event_loop.run_until_complete(create_admin_user())
    payload = f'username={user_data.get("username")}&password={user_data.get("password")}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = client.post('/token', data=payload, headers=headers)
    token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    return headers


@pytest.fixture(scope='module')
def get_admin_headers(client: TestClient, admin_user: dict, event_loop: asyncio.AbstractEventLoop):
    return get_headers(client=client, event_loop=event_loop, user_data=admin_user)


@pytest.fixture(scope='module')
def get_default_headers(client: TestClient, default_user: dict, event_loop: asyncio.AbstractEventLoop):
    return get_headers(client=client, event_loop=event_loop, user_data=default_user)
