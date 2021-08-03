from backend.app.users.models import Profile
from ..fixtures import *
from ..utils import get_obj_from_db, filter_obj_from_db


def test_user_create_profile(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                             create_user_profile: dict, get_default_headers: dict):
    response = client.post('/profile', json=create_user_profile, headers=get_default_headers)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data.get('first_name') == 'test'
    profile_obj = event_loop.run_until_complete(get_obj_from_db(Profile, data))
    assert profile_obj.id == data.get('id')


def test_user_create_profile_unauthenticated(client: TestClient, create_user_profile: dict):
    response = client.post('/profile', json=create_user_profile)
    assert response.status_code == 401


def test_user_get_profile(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                          get_default_headers: dict):
    response = client.get('/profile', headers=get_default_headers)
    assert response.status_code == 200
    data = response.json()
    profile_obj = event_loop.run_until_complete(get_obj_from_db(Profile, data))
    assert profile_obj.id == data.get('id')
    assert data.get('first_name') == 'test'


def test_user_get_profile_unauthenticated(client: TestClient):
    response = client.get('/profile')
    assert response.status_code == 401


def test_user_update_profile(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                             get_default_headers: dict, update_user_profile: dict):
    response = client.put('/profile', json=update_user_profile, headers=get_default_headers)
    assert response.status_code == 200
    data = response.json()
    profile_obj = event_loop.run_until_complete(get_obj_from_db(Profile, data))
    assert profile_obj.id == data.get('id')
    assert data.get('first_name') == 'upd test'


def test_user_update_profile_unauthenticated(client: TestClient, update_user_profile: dict):
    response = client.put('/profile', json=update_user_profile)
    assert response.status_code == 401


def test_user_delete_profile(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_default_headers: dict):
    response = client.delete('/profile', headers=get_default_headers)
    assert response.status_code == 200
    data = response.json()
    profile_list = event_loop.run_until_complete(filter_obj_from_db(Profile, data))
    assert len(profile_list) == 0


def test_user_delete_profile_unauthenticated(client: TestClient):
    response = client.delete('/profile')
    assert response.status_code == 401
