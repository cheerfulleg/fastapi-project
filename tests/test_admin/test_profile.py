import asyncio

import pytest
from starlette.testclient import TestClient

from backend.app.users.models import Profile
from ..conftest import get_default_headers, get_admin_headers

PROFILE_ID = 1


@pytest.fixture()
def create_profile_data() -> dict:
    return {
        "first_name": "test",
        "last_name": "profile",
        "date_of_birth": "2021-07-29",
        "user_id": 1
    }


@pytest.fixture()
def update_profile_data() -> dict:
    return {
        "first_name": "upd test",
        "last_name": "foo",
        "date_of_birth": "2021-07-29",
        "user_id": 1
    }


@pytest.fixture()
def update_profile_data_with_invalid_user_id() -> dict:
    return {
        "first_name": "upd test",
        "last_name": "foo",
        "date_of_birth": "2021-07-29",
        "user_id": 99999999
    }


async def get_profile_from_db(profile_id: int) -> Profile:
    return await Profile.get(id=profile_id)


async def filter_profile_from_db(user_id) -> list:
    return await Profile.filter(id=user_id)


def test_admin_create_profile(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                              create_profile_data: dict, get_admin_headers: dict):

    response = client.post('/admin/profile', json=create_profile_data, headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    profile_id = data.get('id')
    assert data.get('first_name') == 'test'
    profile_obj = event_loop.run_until_complete(get_profile_from_db(profile_id))
    assert profile_obj.id == profile_id


def test_admin_get_profile_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                                 get_admin_headers: dict):
    response = client.get(f'/admin/profile/{PROFILE_ID}', headers=get_admin_headers)
    assert response.status_code == 200
    profile_obj = event_loop.run_until_complete(get_profile_from_db(PROFILE_ID))
    data = response.json()
    assert data.get('first_name') == profile_obj.first_name
    assert data.get('last_name') == profile_obj.last_name


def test_admin_get_list_profile_list(client: TestClient, get_admin_headers: dict):
    response = client.get('/admin/profile', headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list
    assert data[0].get('id') == 1


def test_admin_update_profile_by_id(client: TestClient, get_admin_headers: dict, update_profile_data: dict):
    response = client.put(f'/admin/profile/{PROFILE_ID}', headers=get_admin_headers, json=update_profile_data)
    assert response.status_code == 200
    data = response.json()
    assert data.get('first_name') == 'upd test'
    assert data.get('last_name') == 'foo'


def test_admin_update_profile_by_id_with_invalid_user_id(client: TestClient,
                                                         get_admin_headers: dict,
                                                         update_profile_data_with_invalid_user_id: dict):
    response = client.put(f'/admin/profile/{PROFILE_ID}', headers=get_admin_headers,
                          json=update_profile_data_with_invalid_user_id)
    assert response.status_code == 404


def test_admin_delete_profile_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                                    get_admin_headers: dict):
    response = client.delete(f'/admin/profile/{PROFILE_ID}', headers=get_admin_headers)
    assert response.status_code == 200
    profile_filter = event_loop.run_until_complete(filter_profile_from_db(PROFILE_ID))
    assert len(profile_filter) == 0
