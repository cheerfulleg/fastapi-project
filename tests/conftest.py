from typing import Generator

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.pylint import MODELS
from tortoise.contrib.test import finalizer, initializer

from backend.config.settings import client as mongo_client
from backend.main import app
from tests.utils import clean_mongo


@pytest.fixture(scope="module", autouse=True)
def client() -> Generator:
    initializer(modules=MODELS)  # postgres setup
    with TestClient(app) as c:
        yield c
    finalizer()  # Clean postgres test db
    clean_mongo(mongo_client)  # Clear mongo after tests completed


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
