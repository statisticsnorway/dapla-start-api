FROM python:3.9-alpine

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apk update && apk upgrade && \
    apk add gcc git curl linux-headers musl-dev libffi-dev

RUN pip install --upgrade pip && \
    pip install poetry

WORKDIR /app
COPY . ./

RUN poetry install --no-interaction

EXPOSE 8000
ENTRYPOINT [ "poetry", "run", "uvicorn", "server.api:app", "--host", "0.0.0.0" ]
