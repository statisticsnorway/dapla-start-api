import json
import logging
from subprocess import CalledProcessError

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from .create_jira_issue import ProjectDetails, create_issue_basic
from .emneindeling import get_subject_areas_tree_select

app = FastAPI()
instrumentator = Instrumentator(excluded_handlers=["/health/.*", "/metrics"])
instrumentator.instrument(app).expose(app)

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


@app.get("/subject_areas_tree")
def subject_areas_tree():
    """
    Get a TreeSelect-compatible json containing the statistical subject areas of SSB
    :return:
    """
    logging.info("Got an emneindeling-tree request")
    try:
        return get_subject_areas_tree_select()
    except Exception as error:
        error_text = f"Error occurred while getting statistical subjects tree: {error}"
        logging.error(error_text)
        raise HTTPException(status_code=500, detail=error_text)


@app.post("/create_jira", status_code=201)
def create_issue(details: ProjectDetails):
    """
    Endpoint for Jira issue creation using basic auth
    """
    try:
        logging.info(f"Got a jira issue creation request. Details:\n{details.json()}")
        response_from_jira = create_issue_basic(details)
        logging.debug(response_from_jira)
        return json.loads(response_from_jira.text)
    except (CalledProcessError, Exception) as error:
        logging.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error}")
