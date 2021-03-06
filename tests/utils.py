import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.testclient import TestClient

from backend.app.users.models import User
from backend.app.users.utils import create_password_hash


def clean_mongo(client: AsyncIOMotorClient):
    client.drop_database("tests_chat")


def get_headers(client: TestClient, user_data: dict, event_loop: asyncio.AbstractEventLoop):
    """Setups user in test database, returns auth headers for this user"""

    async def create_admin_user():
        password = create_password_hash(user_data.get("password"))
        return await User.create(**user_data, password_hash=password)

    event_loop.run_until_complete(create_admin_user())
    payload = f'username={user_data.get("username")}&password={user_data.get("password")}'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = client.post("/token", data=payload, headers=headers)
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def get_profile_headers(
    client: TestClient,
    profile_data: dict,
    user_data: dict,
    event_loop: asyncio.AbstractEventLoop,
) -> dict:
    """Creates headers for user with profile"""
    headers = get_headers(client=client, event_loop=event_loop, user_data=user_data)
    client.post("/profile", json=profile_data, headers=headers)
    return headers


async def get_obj_from_db(model, response_json: dict):
    obj_id = response_json.get("id")
    return await model.get(id=obj_id)


async def filter_obj_from_db(model, response_json: dict) -> list:
    obj_id = response_json.get("id")
    return await model.filter(id=obj_id)
