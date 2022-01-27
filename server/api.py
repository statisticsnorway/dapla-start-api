import logging
from subprocess import CalledProcessError

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from requests import HTTPError

from .clients import JiraClient
from .create_jira_issue import ProjectDetails, create_issue_basic

app = FastAPI()
instrumentator = Instrumentator(excluded_handlers=["/health/.*", "/metrics"])
instrumentator.instrument(app).expose(app)


def get_jira_client():
    return JiraClient("https://statistics-norway.atlassian.net/rest/api/3")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health/liveness")
def health_liveness():
    """Can be used to poll for API liveness
    """
    return {
        "name": "dapla-start-api",
        "status": "UP"
    }


@app.get("/health/readiness")
def health_readiness():
    """Can be used to poll for API readiness
    """
    return {
        "name": "dapla-start-api",
        "status": "UP"
    }


@app.post("/create_jira", status_code=201)
def create_issue(details: ProjectDetails, client: JiraClient = Depends(get_jira_client)):
    """
    Endpoint for Jira issue creation using basic auth
    """
    try:
        logging.info(f"Got a jira issue creation request. Details:\n{details.json()}")
        return client.create_issue(create_issue_basic(details))
    except CalledProcessError as error:
        logging.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error.stdout.decode()}")
    except HTTPError as error:
        logging.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error.response.text}")
    except Exception as error:
        logging.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error}")

