import pytest as pytest
from fastapi.testclient import TestClient

from tests.unit import app_test


@pytest.fixture
def client():
    return TestClient(app_test, raise_server_exceptions=False)
