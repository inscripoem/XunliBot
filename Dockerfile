FROM python:3.10

WORKDIR /app

RUN echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free' > /etc/apt/sources.list && \
    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free' >> /etc/apt/sources.list && \
    echo 'deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bullseye-security main contrib non-free' >> /etc/apt/sources.list && \
    apt update

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && python3 -m pip install poetry && poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY . .

CMD cp /app/env/.env.prod /app && nb run