FROM python:3.9-slim

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on


RUN pip install poetry
RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN apt-get update && apt-get install -y --no-install-recommends git

WORKDIR /app
COPY . ./

RUN poetry install --no-interaction

EXPOSE 8000
ENTRYPOINT [ "poetry", "run", "uvicorn", "server.api:app", "--host", "0.0.0.0" ]
