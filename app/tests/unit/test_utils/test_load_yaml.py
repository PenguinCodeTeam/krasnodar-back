import pytest

import yaml
from internal.core.settings.loaders.yaml import __load_yaml


def test_load_yaml_with_valid_data(yaml_path):
    data = __load_yaml(yaml_path)
    assert isinstance(data, dict)
    assert 'param1' in data
    assert 'param2' in data
    assert data['param1'] == 'value1'
    assert data['param2'] == NotImplemented


def test_load_yaml_with_invalid_syntax(yaml_path_wrong_data):
    with pytest.raises(yaml.YAMLError):
        __load_yaml(yaml_path_wrong_data)
