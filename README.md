# Бэкенд для магазина продуктов 
Стек: fastapi, pydantic, sqlalchemy(psycopg2-binary, asyncpg), alembic, sqladmin, aiobotocore, poetry

## Для запуска необходимо выполнить
```shell
python3 -m venv venv
source venv/bin/activate
pip install poetry
poetry install
alembic upgrade head
python3 -m uvicorn app.main:app --reload
```

### Документация
```
http://127.0.0.1:8000/documentation
```

### Админка
```
http://127.0.0.1:8000/admin/
```