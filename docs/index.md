# Локальное развертывание
1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-repo.git
```

2. Перейдите в директорию проекта:
```bash
cd your-repo
```
Добавить в PYTHONPATH путь до модуля app

3. Переопределить настройки в соответствии с рабочим окружением
```bash
cp app/config/local.yaml.tmpl app/config/local.yaml
```

4. Установите poetry, если его еще нет на вашей системе:
```bash
pip install poetry
```

5. Установите зависимости проекта с помощью poetry:
```bash
poetry install --with dev --with test
```

6. Установите переменную окружения ENVIRONMENT в значение "dev". В Linux/macOS это можно сделать следующим образом:
```bash
export ENVIRONMENT=dev
```
А в Windows:
```bash
set ENVIRONMENT=dev
```


8. Запустите тесты с помощью pytest:
```bash
poetry run pytest
```


9. Теперь вы можете запустить сервер FastAPI:
```bash
poetry run python3 app/main.py
```

После запуска сервера FastAPI вы сможете отправлять запросы по адресу `http://localhost:8000/api/ping`, и получите в ответ "PONG".
