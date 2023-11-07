FROM python:3.12.0-slim

ENV PATH="/opt/poetry/bin:/opt/pysetup/.venv/bin:$PATH"

RUN pip install poetry

WORKDIR /project

COPY pyproject.toml .
COPY poetry.lock .

COPY app/ app/
COPY alembic.ini alembic.ini

RUN cp app/config/local.yaml.tmpl app/config/local.yaml
RUN mkdir logs

RUN poetry install

WORKDIR /project

EXPOSE 8000
