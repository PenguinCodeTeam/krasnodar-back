FROM python:3.12.0-slim

ENV PATH="/opt/poetry/bin:/opt/pysetup/.venv/bin:$PATH"

# RUN curl -sSL https://install.python-poetry.org | python3 -
RUN pip install poetry

WORKDIR /project

COPY pyproject.toml .
COPY poetry.lock .

COPY app/ app/
RUN cp app/config/local.yaml.tmpl app/config/local.yaml
RUN mkdir logs

RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "python3", "app/main.py"]
