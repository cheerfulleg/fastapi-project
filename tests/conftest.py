from typing import Generator

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.pylint import MODELS
from tortoise.contrib.test import finalizer, initializer

from backend.main import app


@pytest.fixture(scope="module", autouse=True)
def client() -> Generator:
    initializer(modules=MODELS)
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
