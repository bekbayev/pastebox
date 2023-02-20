FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev

RUN apt-get install -y --no-install-recommends python3-dev gcc curl

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION=1.3.2
ENV PATH="$POETRY_HOME/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry export --with psycopg2-production,test -f requirements.txt --output requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev

COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache /wheels/*

COPY entrypoint.sh ./
COPY src ./src

WORKDIR /app/src

ENTRYPOINT ["../entrypoint.sh"]

CMD ["django-admin", "--version"]