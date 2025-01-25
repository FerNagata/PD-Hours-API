import os

from typing import Generator
from fastapi.testclient import TestClient
import pytest
from main import api
    
# Fixture to instantiate a client
@pytest.fixture(scope="function", autouse=True)
def client() -> Generator:
    with TestClient(api) as client:
        yield client
