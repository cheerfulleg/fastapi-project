from backend.app.users.models import User
from tests.utils import get_obj_from_db
from ..fixtures import *


def test_create_user_unauthenticated(client: TestClient, event_loop: asyncio.AbstractEventLoop,
                                     create_default_user: dict):
    response = client.post('/user', json=create_default_user)
    assert response.status_code == 201
    data = response.json()
    assert data.get("username") == "test"
    assert "id" in data
    user_obj = event_loop.run_until_complete(get_obj_from_db(User, data))
    assert user_obj.id == data.get("id")
    assert user_obj.verify_password(create_default_user.get('password_hash')) is True


def test_create_user_unauthenticated_with_invalid_user_data(client: TestClient, invalid_user_data: dict):
    response = client.post('/user', json=invalid_user_data)
    assert response.status_code == 422
