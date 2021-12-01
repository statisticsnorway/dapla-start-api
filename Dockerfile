FROM python:3.9-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
RUN pip install poetry

WORKDIR /app
COPY . ./

RUN poetry install --no-interaction

EXPOSE 8000
ENTRYPOINT [ "poetry", "run", "uvicorn", "server.api:app", "--host", "0.0.0.0" ]
