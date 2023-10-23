import os
import tempfile

import pytest
from starlette.requests import Request
from starlette.testclient import TestClient

from tests.unit import app_test


@pytest.fixture
async def fake_request(mocker):
    return mocker.Mock(spec=Request)


@pytest.fixture
def client():
    return TestClient(app_test, raise_server_exceptions=False)


@pytest.fixture
def yaml_path():
    data = """
    param1: value1
    param2: !secret
    """

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(data)
        temp_path = f.name

    yield temp_path

    os.remove(temp_path)


@pytest.fixture
def yaml_path_wrong_data():
    data = """
    param1: value1
    param2: value2: value3
    """

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(data)
        temp_path = f.name

    yield temp_path

    os.remove(temp_path)


@pytest.fixture
def data():
    return {
        'login': 'teststestov',
        'password': 'secret_password',
        'message': '1234567890123456',
        'phone': '+15555555555',
        'code': '6989',
    }
