# Backend for coffee shop
Stack: fastapi, pydantic, sqlalchemy(psycopg2-binary), alembic, pyjwt, uv

# Run project
```shell
# creating a virtual environment and installing dependencies
uv sync

# activating virtual environment
source .venv/bin/activate

# rename the env.example to env
mv .env.example .env

# run migrations
alembic upgrade head

# project launch
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Swagger documentation
```
http://localhost:8080/docs
```

