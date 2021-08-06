import asyncio

import pytest
from starlette.testclient import TestClient

from tests.utils import get_headers, get_profile_headers


# Fixtures for test_admin_actions
@pytest.fixture(scope="module")
def create_profile_data() -> dict:
    return {
        "first_name": "test",
        "last_name": "profile",
        "date_of_birth": "2021-07-29",
        "user_id": 1,
    }


@pytest.fixture(scope="module")
def update_profile_data() -> dict:
    return {
        "first_name": "upd test",
        "last_name": "foo",
        "date_of_birth": "2021-07-29",
        "user_id": 1,
    }


@pytest.fixture()
def profile_data_with_invalid_user_id() -> dict:
    return {
        "first_name": "upd test",
        "last_name": "foo",
        "date_of_birth": "2021-07-29",
        "user_id": 99999999,
    }


@pytest.fixture(scope="module")
def create_user_data() -> dict:
    return {
        "username": "test",
        "email": "user@email.com",
        "password_hash": "secret",
        "is_admin": False,
    }


@pytest.fixture(scope="module")
def update_user_data() -> dict:
    return {"username": "update_test", "email": "default@email.com", "is_admin": True}


@pytest.fixture(scope="module")
def admin_user() -> dict:
    return {
        "username": "admin",
        "email": "admin@email.com",
        "password": "secret",
        "is_admin": True,
    }


@pytest.fixture(scope="module")
def default_user() -> dict:
    return {
        "username": "default",
        "email": "default@email.com",
        "password": "secret",
        "is_admin": False,
    }


@pytest.fixture(scope="module")
def profile_user() -> dict:
    return {
        "username": "Profile",
        "email": "has_profile@email.com",
        "password": "secret",
        "is_admin": False,
    }


@pytest.fixture(scope="module")
def post_data() -> dict:
    return {"title": "Dummy title", "body": "lorem ipsum", "profile_id": 1}


@pytest.fixture(scope="module")
def admin_update_post_data() -> dict:
    return {"title": "Update title", "body": "lorem ipsum", "profile_id": 1}


@pytest.fixture(scope="module")
def post_data_with_invalid_profile_id() -> dict:
    return {"title": "Dummy title", "body": "lorem ipsum", "profile_id": 88888}


# Fixtures for test_user_actions
@pytest.fixture(scope="module")
def create_default_user() -> dict:
    return {
        "username": "test",
        "email": "default@email.com",
        "password_hash": "secret",
    }


@pytest.fixture(scope="module")
def create_user_profile() -> dict:
    return {"first_name": "test", "last_name": "profile", "date_of_birth": "2021-07-29"}


@pytest.fixture(scope="module")
def update_user_profile() -> dict:
    return {"first_name": "upd test", "last_name": "foo", "date_of_birth": "2021-07-29"}


@pytest.fixture(scope="module")
def create_post_data() -> dict:
    return {"title": "Dummy title", "body": "lorem ipsum"}


@pytest.fixture(scope="module")
def update_post_data() -> dict:
    return {"title": "Updated post", "body": "some data"}


# Shared fixtures
@pytest.fixture(scope="module")
def invalid_profile_data() -> dict:
    return {"first_name": "invalid", "invalid_field": True}


@pytest.fixture(scope="module")
def invalid_user_data() -> dict:
    return {"username": "invalid", "invalid_field": True}


@pytest.fixture(scope="module")
def invalid_post_data() -> dict:
    return {"title": "Title" * 100}


@pytest.fixture(scope="module")
def get_admin_headers(client: TestClient, admin_user: dict, event_loop: asyncio.AbstractEventLoop) -> dict:
    """Creates headers for admin user"""
    return get_headers(client=client, event_loop=event_loop, user_data=admin_user)


@pytest.fixture(scope="module")
def get_default_headers(client: TestClient, default_user: dict, event_loop: asyncio.AbstractEventLoop) -> dict:
    """Creates headers for default non-profile user"""
    return get_headers(client=client, event_loop=event_loop, user_data=default_user)


@pytest.fixture(scope="module")
def get_user_with_profile_headers(
    client: TestClient,
    profile_user: dict,
    create_user_profile: dict,
    event_loop: asyncio.AbstractEventLoop,
) -> dict:
    """Creates headers for user with profile"""
    return get_profile_headers(client=client, user_data=profile_user, profile_data=create_user_profile, event_loop=event_loop)


@pytest.fixture(scope="module")
def get_admin_with_profile_headers(client: TestClient, admin_user: dict, create_user_profile: dict, event_loop: asyncio.AbstractEventLoop):
    """Creates admin user with profile instance"""
    return get_profile_headers(client=client, user_data=admin_user, profile_data=create_user_profile, event_loop=event_loop)
