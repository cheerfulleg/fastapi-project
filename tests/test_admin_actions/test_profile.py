from backend.app.users.models import Profile
from ..fixtures import *
from ..utils import get_obj_from_db, filter_obj_from_db

PROFILE_ID = 1
INVALID_PROFILE_ID = 99999999


def test_admin_create_profile(
    client: TestClient,
    event_loop: asyncio.AbstractEventLoop,
    create_profile_data: dict,
    get_admin_headers: dict,
):
    response = client.post("/admin/profiles", json=create_profile_data, headers=get_admin_headers)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data.get("first_name") == "test"
    profile_obj = event_loop.run_until_complete(get_obj_from_db(Profile, data))
    assert profile_obj.id == data.get("id")


def test_admin_create_profile_with_invalid_data(client: TestClient, profile_data_with_invalid_user_id: dict, get_admin_headers: dict):
    response = client.post("/admin/profiles", json=profile_data_with_invalid_user_id, headers=get_admin_headers)
    assert response.status_code == 404


def test_admin_create_profile_with_invalid_user_id(client: TestClient, invalid_profile_data: dict, get_admin_headers: dict):
    response = client.post("/admin/profiles", json=invalid_profile_data, headers=get_admin_headers)
    assert response.status_code == 422


def test_admin_create_profile_unauthenticated(client: TestClient, create_profile_data: dict):
    response = client.post("/admin/profiles", json=create_profile_data)
    assert response.status_code == 401


def test_admin_create_profile_not_admin(client: TestClient, create_profile_data: dict, get_default_headers: dict):
    response = client.post("/admin/profiles", headers=get_default_headers, json=create_profile_data)
    assert response.status_code == 403


def test_admin_get_profile_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_admin_headers: dict):
    response = client.get(f"/admin/profiles/{PROFILE_ID}", headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    profile_obj = event_loop.run_until_complete(get_obj_from_db(Profile, data))
    assert data.get("first_name") == profile_obj.first_name
    assert data.get("last_name") == profile_obj.last_name


def test_admin_get_profile_by_invalid_id(client: TestClient, get_admin_headers: dict):
    response = client.get(f"/admin/profiles/{INVALID_PROFILE_ID}", headers=get_admin_headers)
    assert response.status_code == 404


def test_admin_get_profile_by_id_unauthenticated(client: TestClient):
    response = client.get(f"/admin/profiles/{PROFILE_ID}")
    assert response.status_code == 401


def test_admin_get_profile_by_id_not_admin(client: TestClient, get_default_headers: dict):
    response = client.get("/admin/profiles", headers=get_default_headers)
    assert response.status_code == 403


def test_admin_get_list_profile_list(client: TestClient, get_admin_headers: dict):
    response = client.get("/admin/profiles", headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert type(data["items"]) == list
    assert data["items"][0].get("id") == 1


def test_admin_get_list_profile_list_unauthenticated(client: TestClient):
    response = client.get(f"/admin/profiles")
    assert response.status_code == 401


def test_admin_get_list_profile_list_not_admin(client: TestClient, get_default_headers: dict):
    response = client.get("/admin/profiles", headers=get_default_headers)
    assert response.status_code == 403


def test_admin_update_profile_by_id(client: TestClient, get_admin_headers: dict, update_profile_data: dict):
    response = client.put(
        f"/admin/profiles/{PROFILE_ID}",
        headers=get_admin_headers,
        json=update_profile_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("first_name") == "upd test"
    assert data.get("last_name") == "foo"


def test_admin_update_profile_with_invalid_data(client: TestClient, get_admin_headers: dict, invalid_profile_data: dict):
    response = client.put(
        f"/admin/profiles/{PROFILE_ID}",
        json=invalid_profile_data,
        headers=get_admin_headers,
    )
    assert response.status_code == 422


def test_admin_update_profile_by_invalid_id(client: TestClient, get_admin_headers: dict, update_profile_data: dict):
    response = client.get(
        f"/admin/profiles/{INVALID_PROFILE_ID}",
        headers=get_admin_headers,
        json=update_profile_data,
    )
    assert response.status_code == 404


def test_admin_update_profile_by_id_unauthenticated(client: TestClient, update_profile_data: dict):
    response = client.put(f"/admin/profiles/{PROFILE_ID}", json=update_profile_data)
    assert response.status_code == 401


def test_admin_update_profile_by_id_not_admin(client: TestClient, get_default_headers: dict, update_profile_data: dict):
    response = client.put(
        f"/admin/profiles/{PROFILE_ID}",
        json=update_profile_data,
        headers=get_default_headers,
    )
    assert response.status_code == 403


def test_admin_update_profile_by_id_with_invalid_user_id(
    client: TestClient,
    get_admin_headers: dict,
    profile_data_with_invalid_user_id: dict,
):
    response = client.put(
        f"/admin/profiles/{PROFILE_ID}",
        headers=get_admin_headers,
        json=profile_data_with_invalid_user_id,
    )
    assert response.status_code == 404


def test_admin_delete_profile_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_admin_headers: dict):
    response = client.delete(f"/admin/profiles/{PROFILE_ID}", headers=get_admin_headers)
    assert response.status_code == 200
    data = response.json()
    profile_filter = event_loop.run_until_complete(filter_obj_from_db(Profile, data))
    assert len(profile_filter) == 0


def test_admin_delete_profile_by_invalid_id(client: TestClient, get_admin_headers: dict):
    response = client.delete(f"/admin/profiles/{INVALID_PROFILE_ID}", headers=get_admin_headers)
    assert response.status_code == 404


def test_admin_delete_profile_by_id_unauthenticated(client: TestClient):
    response = client.delete(f"/admin/profiles/{PROFILE_ID}")
    assert response.status_code == 401


def test_admin_delete_profile_by_id_not_admin(client: TestClient, get_default_headers: dict):
    response = client.delete(f"/admin/profiles/{PROFILE_ID}", headers=get_default_headers)
    assert response.status_code == 403
