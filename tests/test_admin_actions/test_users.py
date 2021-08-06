from backend.app.users.models import User
from ..fixtures import *
from ..utils import get_obj_from_db, filter_obj_from_db

USER_ID = 2
INVALID_USER_ID = 9999999


def test_admin_create_user(
    client: TestClient,
    event_loop: asyncio.AbstractEventLoop,
    create_user_data: dict,
    get_admin_headers: dict,
):
    response = client.post("/admin/users", json=create_user_data, headers=get_admin_headers)
    assert response.status_code == 201
    data = response.json()
    assert data.get("username") == "test"
    assert "id" in data

    user_obj = event_loop.run_until_complete(get_obj_from_db(User, data))
    assert user_obj.id == data.get("id")
    assert user_obj.verify_password(create_user_data.get("password_hash")) is True


def test_admin_create_user_with_invalid_data(client: TestClient, invalid_user_data: dict, get_admin_headers: dict):
    response = client.post("/admin/users", json=invalid_user_data, headers=get_admin_headers)
    assert response.status_code == 422


def test_admin_create_user_unauthenticated(client: TestClient, create_user_data: dict):
    response = client.post("/admin/users", json=create_user_data)
    assert response.status_code == 401


def test_admin_create_user_not_admin(client: TestClient, get_default_headers: dict, create_user_data: dict):
    response = client.post("/admin/users", json=create_user_data, headers=get_default_headers)
    assert response.status_code == 403


def test_admin_get_user_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_admin_headers: dict):
    response = client.get(f"/admin/users/{USER_ID}", headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    user_obj = event_loop.run_until_complete(get_obj_from_db(User, data))
    assert user_obj.username == data.get("username")
    assert data.get("username") == "test"


def test_admin_get_user_by_invalid_id(client: TestClient, get_admin_headers: dict):
    response = client.get(f"/admin/users/{INVALID_USER_ID}", headers=get_admin_headers)
    assert response.status_code == 404


def test_admin_get_user_by_id_unauthenticated(client: TestClient):
    response = client.get(f"/admin/users/{USER_ID}")
    assert response.status_code == 401


def test_admin_get_user_by_id_not_admin(client: TestClient, get_default_headers: dict):
    response = client.get(f"/admin/users/{USER_ID}", headers=get_default_headers)
    assert response.status_code == 403


def test_admin_get_user_list(client: TestClient, get_admin_headers: dict):
    response = client.get("/admin/users", headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert type(data) == list
    assert data[0].get("username") == "admin"
    assert data[1].get("username") == "test"


def test_admin_get_user_list_unauthenticated(client: TestClient):
    response = client.get("/admin/users")
    assert response.status_code == 401


def test_admin_get_user_list_not_admin(client: TestClient, get_default_headers: dict):
    response = client.get("/admin/users", headers=get_default_headers)
    assert response.status_code == 403


def test_admin_update_user_by_id(
    client: TestClient,
    event_loop: asyncio.AbstractEventLoop,
    get_admin_headers: dict,
    update_user_data: dict,
):
    response = client.put(f"/admin/users/{USER_ID}", headers=get_admin_headers, json=update_user_data)
    assert response.status_code == 200
    data = response.json()
    user_obj = event_loop.run_until_complete(get_obj_from_db(User, data))
    assert data.get("username") == "update_test"
    assert data.get("username") == user_obj.username


def test_admin_update_user_by_invalid_id(client: TestClient, update_user_data: dict, get_admin_headers: dict):
    response = client.put(
        f"/admin/users/{INVALID_USER_ID}",
        json=update_user_data,
        headers=get_admin_headers,
    )
    assert response.status_code == 404


def test_admin_update_user_by_id_with_invalid_data(client: TestClient, invalid_user_data: dict, get_admin_headers: dict):
    response = client.put(f"/admin/users/{USER_ID}", json=invalid_user_data, headers=get_admin_headers)
    assert response.status_code == 422


def test_admin_update_user_by_id_unauthenticated(client: TestClient, create_user_data: dict):
    response = client.put(f"/admin/users/{USER_ID}", json=create_user_data)
    assert response.status_code == 401


def test_admin_update_user_by_id_not_admin(client: TestClient, get_default_headers: dict, create_user_data: dict):
    response = client.put(f"/admin/users/{USER_ID}", json=create_user_data, headers=get_default_headers)
    assert response.status_code == 403


def test_admin_delete_user_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_admin_headers: dict):
    response = client.delete(f"/admin/users/{USER_ID}", headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    user_filter = event_loop.run_until_complete(filter_obj_from_db(User, data))
    assert len(user_filter) == 0


def test_admin_delete_user_by_invalid_id(client: TestClient, get_admin_headers: dict):
    response = client.delete(f"/admin/profile/{INVALID_USER_ID}", headers=get_admin_headers)
    assert response.status_code == 404


def test_admin_delete_user_by_id_unauthenticated(client: TestClient):
    response = client.delete(f"/admin/profile/{USER_ID}")
    assert response.status_code == 401


def test_admin_delete_user_by_id_not_admin(client: TestClient, get_default_headers: dict):
    response = client.delete(f"/admin/profile/{USER_ID}", headers=get_default_headers)
    assert response.status_code == 403
