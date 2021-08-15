from bson import ObjectId

from ..fixtures import *

PROFILE_ID = 2
INVALID_PROFILE_ID = 9999


def test_get_chat_by_id(client: TestClient, event_loop: asyncio.AbstractEventLoop, get_user_with_profile_headers: dict, get_admin_with_profile_headers: dict):
    response = client.get(
        f"/chats/{PROFILE_ID}",
        headers=get_user_with_profile_headers,
    )
    assert response.status_code == 200
    data = response.json()
    _id = data.get("_id")

    async def get_chat(_id):
        return await ChatService.get({"_id": ObjectId(_id)})

    chat_from_db = event_loop.run_until_complete(get_chat(_id))
    assert data.get("members") == chat_from_db.get("members")


def test_get_chat_by_invalid_id(client: TestClient, get_user_with_profile_headers: dict):
    response = client.get(
        f"/chats/{INVALID_PROFILE_ID}",
        headers=get_user_with_profile_headers,
    )
    assert response.status_code == 404


def test_get_chat_by_id_unauthenticated(client: TestClient):
    response = client.get(f"/chats/{PROFILE_ID}")
    assert response.status_code == 401


def test_get_chat_by_id_unauthorized(client: TestClient, get_default_headers: dict):
    response = client.get(f"/chats/{PROFILE_ID}", headers=get_default_headers)
    assert response.status_code == 403


def test_get_profile_chats(client: TestClient, get_user_with_profile_headers: dict):
    response = client.get("/chats", headers=get_user_with_profile_headers)
    assert response.status_code == 200
    data = response.json()

    assert type(data) == list
    assert data[0].get("members") == [1, 2]


def test_get_profile_unauthenticated(client: TestClient):
    response = client.get("/chats")
    assert response.status_code == 401


def test_get_profile_unauthorized(client: TestClient, get_default_headers: dict):
    response = client.get("/chats", headers=get_default_headers)
    assert response.status_code == 403


def test_send_message(client: TestClient, get_user_with_profile_headers: dict, chat_id: str, message_body: dict):
    response = client.post(f"/chats/{chat_id}/messages", headers=get_user_with_profile_headers, json=message_body)
    assert response.status_code == 200
    data = response.json()

    assert data.get("body") == "lorem ipsum"
    assert data.get("edited") is False


def test_send_message_unauthenticated(client: TestClient, chat_id: str, message_body: dict):
    response = client.post(f"/chats/{chat_id}/messages", json=message_body)
    assert response.status_code == 401


def test_send_message_unauthorized(client: TestClient, get_default_headers: dict, chat_id: str, message_body: dict):
    response = client.post(f"/chats/{chat_id}/messages", headers=get_default_headers, json=message_body)
    assert response.status_code == 403


def test_send_message_with_invalid_data(client: TestClient, get_user_with_profile_headers: dict, chat_id: str, invalid_message_body: dict):
    response = client.post(f"/chats/{chat_id}/messages", headers=get_user_with_profile_headers, json=invalid_message_body)
    assert response.status_code == 422


def test_get_chat_messages(client: TestClient, get_user_with_profile_headers: dict, chat_id: str):
    response = client.get(f"/chats/{chat_id}/messages", headers=get_user_with_profile_headers)
    assert response.status_code == 200
    data = response.json()

    assert type(data) == list
    assert data[0].get("body") == "lorem ipsum"


def test_get_chat_messages_unauthenticated(client: TestClient, chat_id: str):
    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 401


def test_get_chat_messages_unauthorized(client: TestClient, get_default_headers: dict, chat_id: str):
    response = client.get(f"/chats/{chat_id}/messages", headers=get_default_headers)
    assert response.status_code == 403


def test_get_invalid_chat_id_messages(client: TestClient, get_user_with_profile_headers: dict, invalid_chat_id: str):
    response = client.get(f"/chats/{invalid_chat_id}/messages", headers=get_user_with_profile_headers)
    assert response.status_code == 404


def test_update_message_by_id(client: TestClient, get_user_with_profile_headers: dict, chat_id: str, message_id: str, update_message_body: dict):
    response = client.put(f"/chats/{chat_id}/messages/{message_id}", headers=get_user_with_profile_headers, json=update_message_body)
    assert response.status_code == 200
    data = response.json()

    assert data.get("body") == "UPDATE"
    assert data.get("edited") is True


def test_update_message_unauthenticated(client: TestClient, chat_id: str, message_id: str, update_message_body: dict):
    response = client.put(f"/chats/{chat_id}/messages/{message_id}", json=update_message_body)
    assert response.status_code == 401


def test_update_message_unauthorized(client: TestClient, chat_id: str, message_id: str, get_default_headers: dict, update_message_body: dict):
    response = client.put(f"/chats/{chat_id}/messages/{message_id}", headers=get_default_headers, json=update_message_body)
    assert response.status_code == 403


def test_update_message_by_invalid_id(client: TestClient, get_user_with_profile_headers: dict, chat_id: dict, invalid_message_id: str, update_message_body: dict):
    response = client.put(f"/chats/{chat_id}/messages/{invalid_message_id}", headers=get_user_with_profile_headers, json=update_message_body)
    assert response.status_code == 404


def test_update_message_by_id_with_invalid_chat_id(client: TestClient, get_user_with_profile_headers: dict, invalid_chat_id: dict, message_id: str, update_message_body: dict):
    response = client.put(f"/chats/{invalid_chat_id}/messages/{message_id}", headers=get_user_with_profile_headers, json=update_message_body)
    assert response.status_code == 404


def test_delete_message_by_id(client: TestClient, get_user_with_profile_headers: dict, chat_id: str, message_id: str):
    response = client.delete(f"/chats/{chat_id}/messages/{message_id}", headers=get_user_with_profile_headers)
    assert response.status_code == 200


def test_delete_message_by_invalid_id(client: TestClient, get_user_with_profile_headers: dict, chat_id: dict, invalid_message_id: str):
    response = client.delete(f"/chats/{chat_id}/messages/{invalid_message_id}", headers=get_user_with_profile_headers)
    assert response.status_code == 404


def test_delete_message_by_id_with_invalid_chat_id(client: TestClient, get_user_with_profile_headers: dict, invalid_chat_id: dict, message_id: str):
    response = client.delete(f"/chats/{invalid_chat_id}/messages/{message_id}", headers=get_user_with_profile_headers)
    assert response.status_code == 404


def test_delete_message_unauthenticated(client: TestClient, chat_id: str, message_id: str):
    response = client.delete(f"/chats/{chat_id}/messages/{message_id}")
    assert response.status_code == 401


def test_delete_message_unauthorized(client: TestClient, chat_id: str, message_id: str, get_default_headers: dict):
    response = client.delete(f"/chats/{chat_id}/messages/{message_id}", headers=get_default_headers)
    assert response.status_code == 403
