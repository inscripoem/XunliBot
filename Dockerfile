FROM python:3.10-alpine

WORKDIR /app

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && python3 -m pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY . .

CMD cp /app/env/.env.prod /app && nb run