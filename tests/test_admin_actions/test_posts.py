from backend.app.posts.models import Post
from tests.utils import get_obj_from_db, filter_obj_from_db
from ..fixtures import *

POST_ID = 1
INVALID_POST_ID = 99999


def test_admin_create_post(
    client: TestClient,
    event_loop: asyncio.AbstractEventLoop,
    post_data: dict,
    get_admin_with_profile_headers: dict,
):
    response = client.post("/admin/posts", json=post_data, headers=get_admin_with_profile_headers)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data.get("title") == "Dummy title"
    post_obj = event_loop.run_until_complete(get_obj_from_db(Post, data))
    assert post_obj.id == data.get("id")


def test_admin_create_post_with_invalid_data(
    client: TestClient,
    invalid_post_data: dict,
    get_admin_with_profile_headers: dict,
):
    response = client.post("/admin/posts", json=invalid_post_data, headers=get_admin_with_profile_headers)
    assert response.status_code == 422


def test_admin_create_post_with_invalid_profile_id(
    client: TestClient,
    post_data_with_invalid_profile_id: dict,
    get_admin_with_profile_headers: dict,
):
    response = client.post("/admin/posts", json=post_data_with_invalid_profile_id, headers=get_admin_with_profile_headers)
    assert response.status_code == 404


def test_admin_create_post_unauthenticated(client: TestClient, post_data: dict):
    response = client.post("/admin/profiles", json=post_data)
    assert response.status_code == 401


def test_admin_create_post_not_admin(client: TestClient, post_data: dict, get_default_headers: dict):
    response = client.post("/admin/profiles", json=post_data, headers=get_default_headers)
    assert response.status_code == 403


def test_admin_get_posts_list(client: TestClient, get_admin_with_profile_headers: dict):
    response = client.get("/admin/posts", headers=get_admin_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    assert type(data["items"]) == list
    assert data["items"][0].get("id") == 1


def test_admin_get_posts_list_unauthenticated(client: TestClient, post_data: dict):
    response = client.get("/admin/profiles", json=post_data)
    assert response.status_code == 401


def test_admin_get_post_list_not_admin(client: TestClient, post_data: dict, get_default_headers: dict):
    response = client.get("/admin/profiles", json=post_data, headers=get_default_headers)
    assert response.status_code == 403


def test_admin_get_post_by_id(client: TestClient, get_admin_with_profile_headers: dict):
    response = client.get(f"/admin/posts/{POST_ID}", headers=get_admin_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("title") == "Dummy title"


def test_admin_get_post_by_id_unauthenticated(client: TestClient, post_data: dict):
    response = client.get(f"/admin/profiles/{Post}", json=post_data)
    assert response.status_code == 401


def test_admin_get_post_by_id_not_admin(client: TestClient, post_data: dict, get_default_headers: dict):
    response = client.get(f"/admin/profiles/{POST_ID}", json=post_data, headers=get_default_headers)
    assert response.status_code == 403


def test_admin_update_post_by_id(client: TestClient, admin_update_post_data: dict, get_admin_with_profile_headers: dict):
    response = client.put(f"/admin/posts/{POST_ID}", json=admin_update_post_data, headers=get_admin_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    assert data.get("title") == "Update title"
    assert data.get("profile_id") == 1


def test_admin_update_post_by_invalid_id(client: TestClient, admin_update_post_data: dict, get_admin_with_profile_headers: dict):
    response = client.put(f"/admin/posts/{INVALID_POST_ID}", json=admin_update_post_data, headers=get_admin_with_profile_headers)
    assert response.status_code == 404


def test_admin_update_post_by_id_with_invalid_data(client: TestClient, invalid_post_data: dict, get_admin_with_profile_headers: dict):
    response = client.put(f"/admin/posts/{INVALID_POST_ID}", json=invalid_post_data, headers=get_admin_with_profile_headers)
    assert response.status_code == 422


def test_admin_update_post_by_id_with_invalid_profile_id(
    client: TestClient,
    post_data_with_invalid_profile_id: dict,
    get_admin_with_profile_headers: dict,
):
    response = client.post("/admin/posts", json=post_data_with_invalid_profile_id, headers=get_admin_with_profile_headers)
    assert response.status_code == 404


def test_admin_update_post_by_id_unauthenticated(client: TestClient, admin_update_post_data: dict):
    response = client.put(f"/admin/posts/{POST_ID}", json=admin_update_post_data)
    assert response.status_code == 401


def test_admin_update_post_by_id_not_admin(client: TestClient, admin_update_post_data: dict, get_default_headers: dict):
    response = client.put(f"/admin/posts/{POST_ID}", json=admin_update_post_data, headers=get_default_headers)
    assert response.status_code == 403


def test_admin_delete_post_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_admin_with_profile_headers: dict):
    response = client.delete(f"/admin/posts/{POST_ID}", headers=get_admin_with_profile_headers)
    assert response.status_code == 200
    data = response.json()
    post_filter = event_loop.run_until_complete(filter_obj_from_db(Post, data))
    assert len(post_filter) == 0


def test_admin_delete_post_by_invalid_id(client: TestClient, get_admin_with_profile_headers: dict):
    response = client.delete(f"/admin/posts/{INVALID_POST_ID}", headers=get_admin_with_profile_headers)
    assert response.status_code == 404


def test_admin_delete_post_by_id_unauthenticated(client: TestClient, admin_update_post_data: dict):
    response = client.delete(f"/admin/posts/{POST_ID}", json=admin_update_post_data)
    assert response.status_code == 401


def test_admin_delete_post_by_id_not_admin(client: TestClient, get_default_headers: dict):
    response = client.delete(f"/admin/posts/{POST_ID}", headers=get_default_headers)
    assert response.status_code == 403
