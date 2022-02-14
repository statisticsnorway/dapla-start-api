FROM python:3.9.10-slim

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry
RUN apt update && \
    apt-get -y clean all && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y dist-upgrade && \
    apt-get install -y --no-install-recommends gcc git curl

WORKDIR /app
COPY . ./

RUN poetry install --no-interaction

EXPOSE 8000
ENTRYPOINT [ "poetry", "run", "uvicorn", "server.api:app", "--host", "0.0.0.0" ]
