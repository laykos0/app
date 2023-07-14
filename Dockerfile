FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y build-essential


RUN pip install --no-cache-dir --upgrade setuptools poetry

RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

COPY ./ ./

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
