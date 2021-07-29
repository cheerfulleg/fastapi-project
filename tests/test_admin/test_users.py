import asyncio

import pytest
from starlette.testclient import TestClient

from backend.app.users.models import User
from ..conftest import get_default_headers, get_admin_headers


@pytest.fixture()
def create_user_data() -> dict:
    return {
        "username": "test",
        "password_hash": "secret",
        "is_admin": False
    }


@pytest.fixture()
def update_user_data() -> dict:
    return {
        "username": "update_test",
        "is_admin": True
    }


async def get_user_from_db(user_id: int) -> User:
    return await User.get(id=user_id)


async def filter_user_from_db(user_id):
    return await User.filter(id=user_id)


def test_admin_create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                           create_user_data: dict, get_admin_headers: dict):
    response = client.post("/admin/users",
                           json=create_user_data,
                           headers=get_admin_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "test"
    assert "id" in data
    user_id = data["id"]

    user_obj = event_loop.run_until_complete(get_user_from_db(user_id))
    assert user_obj.id == user_id
    assert user_obj.verify_password(create_user_data.get('password_hash')) is True


def test_get_user_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                        get_admin_headers: dict):
    user_id = 3
    response = client.get(f'/admin/users/{user_id}', headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    user_obj = event_loop.run_until_complete(get_user_from_db(user_id))
    assert user_obj.username == data.get('username')
    assert data.get('username') == 'test'


def test_get_user_list(client: TestClient, get_admin_headers: dict):
    response = client.get('/admin/users', headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list
    assert data[0].get('username') == 'admin'
    assert data[2].get('username') == 'test'


def test_update_user_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                           get_admin_headers: dict, update_user_data: dict):
    user_id = 3
    response = client.put(f'/admin/users/{user_id}', headers=get_admin_headers, json=update_user_data)
    assert response.status_code == 200
    data = response.json()
    user_obj = event_loop.run_until_complete(get_user_from_db(user_id))
    assert data.get('username') == 'update_test'
    assert data.get('username') == user_obj.username


def test_delete_user_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_admin_headers: dict):
    user_id = 3
    response = client.delete(f'/admin/users/{user_id}', headers=get_admin_headers)
    assert response.status_code == 200
    user_filter = event_loop.run_until_complete(filter_user_from_db(user_id))
    assert user_filter == []


def test_access_admin_unauthenticated(client: TestClient):
    response = client.get('/admin/users')
    assert response.status_code == 401


def test_access_admin_as_default_user(client: TestClient, get_default_headers: dict):
    response = client.get('/admin/users', headers=get_default_headers)
    assert response.status_code == 403
