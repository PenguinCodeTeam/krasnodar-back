import sys
from typing import Any


def validate_config(config_module):
    """Валидатор значений параметров конфигурации
    Args:
        config_module: модуль конфигурации приложения
    Raises:
        NameError
    """
    errors = []
    for name, value in config_module.__dict__.items():
        if '__' in name:
            continue
        if not isinstance(value, dict):
            if has_error(value):
                errors.append(name)
        else:
            for nested_name, nested_value in value.items():
                if field := has_error(nested_value):
                    errors.append(f'{name}.{nested_name}.{field}')

    if errors:
        raise NameError(errors)


def has_error(value: Any) -> bool | str:
    if value is NotImplemented:
        return True
    if isinstance(value, dict):
        for nested_key, nested_value in value.items():
            if has_error(nested_value):
                return nested_key
    return False


def validate_config_with_default(default: dict, from_file: dict, filename: str):
    """Валидатор проверяет есть параметр загруженный из файла в дефолтных настройках
    Args:
        default: дефолтные параметры
        from_file: параметры из файла
        filename: имя файла настроек
    """
    for arg in from_file:
        if arg not in default:
            sys.stderr.write(f'{arg} from {filename} not in default settings\n')
