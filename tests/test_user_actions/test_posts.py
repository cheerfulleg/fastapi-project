from backend.app.posts.models import Post
from ..fixtures import *
from ..utils import get_obj_from_db, filter_obj_from_db

POST_ID = 1
INVALID_POST_ID = 99999


def test_profile_create_post(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                             create_post_data: dict, get_user_with_profile_headers: dict):
    response = client.post('/posts', json=create_post_data, headers=get_user_with_profile_headers)
    assert response.status_code == 201
    data = response.json()
    assert 'id' in data
    assert data.get('title') == 'Dummy title'
    post_obj = event_loop.run_until_complete(get_obj_from_db(Post, data))
    assert post_obj.id == data.get('id')


def test_user_no_profile_create_post(client: TestClient, get_default_headers: dict,
                                     create_post_data: dict):
    response = client.post('/posts', json=create_post_data, headers=get_default_headers)
    assert response.status_code == 403


def test_unauthenticated_user_create_post(client: TestClient, create_post_data: dict):
    response = client.post('/posts', json=create_post_data)
    assert response.status_code == 401


def test_profile_create_invalid_post(client: TestClient,
                                     invalid_post_data: dict, get_user_with_profile_headers: dict):
    response = client.post('/posts', json=invalid_post_data, headers=get_user_with_profile_headers)
    assert response.status_code == 422


def test_profile_get_post_by_id(client: TestClient, get_user_with_profile_headers: dict):
    response = client.get(f'/posts/{POST_ID}', headers=get_user_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get('title') == 'Dummy title'


def test_profile_get_post_by_invalid_id(client: TestClient, get_user_with_profile_headers: dict):
    response = client.get(f'/posts/{INVALID_POST_ID}', headers=get_user_with_profile_headers)
    assert response.status_code == 404


def test_user_no_profile_get_post_by_id(client: TestClient, get_default_headers: dict):
    response = client.get(f'/posts/{POST_ID}', headers=get_default_headers)
    assert response.status_code == 403


def test_unauthenticated_user_get_post_by_id(client: TestClient):
    response = client.get(f'/posts/{POST_ID}')
    assert response.status_code == 401


def test_profile_get_posts_list(client: TestClient, get_user_with_profile_headers: dict):
    response = client.get('/posts', headers=get_user_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list
    assert data[0].get('id') == 1


def test_user_no_profile_get_posts_list(client: TestClient, get_default_headers: dict):
    response = client.get('/posts', headers=get_default_headers)
    assert response.status_code == 403


def test_unauthenticated_user_get_posts_list(client: TestClient):
    response = client.get('/posts')
    assert response.status_code == 401


def test_profile_update_update_post_by_id(client: TestClient, get_user_with_profile_headers: dict,
                                          update_post_data: dict):
    response = client.put(f'/posts/{POST_ID}', json=update_post_data, headers=get_user_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get('title') == 'Updated post'


def test_profile_update_update_post_by_invalid_id(client: TestClient, get_user_with_profile_headers: dict,
                                                  update_post_data: dict):
    response = client.put(f'/posts/{INVALID_POST_ID}', json=update_post_data, headers=get_user_with_profile_headers)
    assert response.status_code == 404


def test_profile_update_update_post_by_id_invalid_data(client: TestClient, get_user_with_profile_headers: dict,
                                                       invalid_post_data: dict):
    response = client.put(f'/posts/{INVALID_POST_ID}', json=invalid_post_data, headers=get_user_with_profile_headers)
    assert response.status_code == 422


def test_user_no_profile_update_post_by_id(client: TestClient, get_default_headers: dict, update_post_data: dict):
    response = client.put(f'/posts/{POST_ID}', headers=get_default_headers, json=update_post_data)
    assert response.status_code == 403


def test_unauthenticated_user_update_post_by_id(client: TestClient, update_post_data: dict):
    response = client.put(f'/posts/{POST_ID}', json=update_post_data)
    assert response.status_code == 401


def test_profile_delete_post_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                                   get_user_with_profile_headers: dict):
    response = client.delete(f'/posts/{POST_ID}', headers=get_user_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    post_filter = event_loop.run_until_complete(filter_obj_from_db(Post, data))
    assert len(post_filter) == 0


def test_profile_delete_post_by_invalid_id(client: TestClient, get_user_with_profile_headers: dict):
    response = client.delete(f'/posts/{INVALID_POST_ID}', headers=get_user_with_profile_headers)
    assert response.status_code == 404


def test_user_no_profile_delete_post_by_id(client: TestClient, get_default_headers: dict, update_post_data: dict):
    response = client.delete(f'/posts/{POST_ID}', headers=get_default_headers, json=update_post_data)
    assert response.status_code == 403


def test_unauthenticated_user_delete_post_by_id(client: TestClient, update_post_data: dict):
    response = client.delete(f'/posts/{POST_ID}', json=update_post_data)
    assert response.status_code == 401
