import os
import sys
from pathlib import Path

import config
from internal.core.settings.loaders.yaml import __load_yaml
from internal.core.settings.validators import validate_config_with_default


LOCAL_CONFIG_PATH = f'{Path.cwd()}/config/local.yaml'
LOCAL_CONFIG_TEMPLATE_PATH = f'{Path.cwd()}/config/local.yaml.tmpl'


def load_config(container: dict, filename: str):
    if os.path.exists(filename):
        from_file = __load_yaml(filename)
        validate_config_with_default(default=container, from_file=from_file, filename=filename)
        container.update(from_file)
        sys.stderr.write(f'Loaded config overrides from {filename}\n')
    if os.path.exists(LOCAL_CONFIG_TEMPLATE_PATH) and config.CHECK_CONFIG:
        sys.stderr.write('Check difference with local config and template\n')
        local_yaml = __load_yaml(LOCAL_CONFIG_PATH)
        local_yaml_tmpl = __load_yaml(LOCAL_CONFIG_TEMPLATE_PATH)
        validate_config_with_default(default=local_yaml, from_file=local_yaml_tmpl, filename='local.yaml.tmpl')
