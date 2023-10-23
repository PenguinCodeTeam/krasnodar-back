from unittest.mock import patch

from config import APP_DIR
from internal.core.settings.loaders import local


def test_load_config_local():
    config_data = {'key1': 'value1', 'key2': 'value2'}

    with patch('internal.core.settings.loaders.local.__load_yaml', return_value=config_data):
        container = {}
        local.load_config(container, filename=f'{APP_DIR}/config/local.yaml')

        assert container == config_data


def test_multiply_clients_config_load():
    local_config_test_client = {'key': 'local_value'}
    local_config_other_test_client = {'key': 'other_client_value1', 'key2': 'cluster_value2'}
    container = {}
    with patch('internal.core.settings.loaders.local.__load_yaml', return_value=local_config_test_client):
        local.load_config(container, filename=f'{APP_DIR}/config/local.yaml')
        with patch('internal.core.settings.loaders.local.__load_yaml', return_value=local_config_other_test_client), patch('os.path.exists', return_value=True):
            local.load_config(container, filename=f'{APP_DIR}/config/local.yaml')

        assert container == local_config_test_client | local_config_other_test_client
