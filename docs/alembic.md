# Работа с alembic
1. Создание миграций
```bash
poetry run alembic revision --autogenerate --message "Сообщение миграции"
```

2. Накатить все миграции:
```bash
poetry run alembic upgrade head
```

3. Накатить миграции до определенной версии:
```bash
poetry run alembic upgrade <revision_id>
```

4. Откатить миграцию на одну назад:
```bash
poetry run alembic downgrade -1
```

5. Откатить миграции до определенной версии:
```bash
poetry run alembic downgrade <revision_id>
```
