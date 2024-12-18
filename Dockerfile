FROM python:3.11-slim

WORKDIR /app
EXPOSE 8000

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install --no-install-recommends -y build-essential


RUN pip install --no-cache-dir --upgrade setuptools poetry

RUN poetry config virtualenvs.create false
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install

COPY ./src/ ./src/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
