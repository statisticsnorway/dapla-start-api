import csv
import os
from server import __version__
from subprocess import CalledProcessError

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from requests import HTTPError
from typing import Optional

from .clients import JiraClient, KlassClient
from .project_details import ProjectDetails, project_user_from_jwt
from .create_jira_issue import create_issue_basic
from .org_info import produce_org_info, get_klass_sectional_division
from .config import logger, configure_loggers

SSB_USERS_SOURCE = os.environ.get("SSB_USERS_SOURCE", "tests/test-users-export.csv")

configure_loggers()
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    Instrumentator(excluded_handlers=["/health/.*", "/metrics"]).instrument(app).expose(app)


def get_jira_client():
    return JiraClient("https://statistics-norway.atlassian.net/rest/api/3")


def get_klass_client():
    return KlassClient("https://data.ssb.no/api/klass/v1")


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
def create_issue(details: ProjectDetails, authorization: Optional[str] = Header(None),
                 client: JiraClient = Depends(get_jira_client)):
    """
    Endpoint for Jira issue creation using basic auth
    """
    try:
        logger.info(f"Got a jira issue creation request. Details:\n{details.json(indent=2)}")
        if authorization is not None:
            bearer, _, token = authorization.partition(' ')
            details.reporter = project_user_from_jwt(token)
            logger.info(f"Reported by: %s" % details.reporter)

        details.api_version = __version__
        return client.create_issue(create_issue_basic(details))
    except CalledProcessError as error:
        logger.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error.stdout.decode()}")
    except HTTPError as error:
        logger.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error.response.text}")
    except Exception as error:
        logger.exception("Error occurred: %s", error)
        raise HTTPException(status_code=500, detail=f"Error occurred:\n\n{error}")


@app.get("/users")
def list_users(fields: str = None):
    """List all applicable SSB users.

    Only return users that:
    * Has a valid first- and surname
    * Has an active account
    * Has a short email starting with 3 letters OR has a "kons" prefix
    """
    all_fields = set(["name", "email", "email_short"])
    fields_filter = set([f.strip() for f in fields.split(',')]) if fields else all_fields
    fields_filter = fields_filter.intersection(all_fields)
    if len(fields_filter) == 0:
        fields_filter = all_fields

    users = []
    with open(SSB_USERS_SOURCE, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1

            skip = False
            display_name = row["displayName"].strip()
            principal = row['userPrincipalName'].strip()

            # Skip users without proper name
            if len(display_name) == 0:
                skip = True

            # Only keep accounts with principals with "3-letter" and those starting with "kons"
            elif not (len(principal) > 4 and (principal[3] == '@' or principal.startswith('kons'))):
                skip = True

            if not skip:
                user = {}

                if 'name' in fields_filter:
                    user['name'] = display_name.replace("  ", ", ", 1)

                if 'email' in fields_filter:
                    user['email'] = str(row['mail']).lower()

                if 'email_short' in fields_filter:
                    user['email_short'] = principal

                users.append(user)

            line_count += 1

    return users


@app.get("/org_info", status_code=200)
def list_org_info(client: KlassClient = Depends(get_klass_client)):
    """List organization information
    """
    try:
        sectional_division_versions = client.get_sectional_division_versions()
        newest_version_url = get_klass_sectional_division(sectional_division_versions)
        newest_version_data = client.get_latest_sectional_division_version(newest_version_url)

        return produce_org_info(newest_version_data)
    except Exception as error:
        error_text = f"Error occurred while getting organization information: {error}"
        logger.error(error_text)

        raise HTTPException(status_code=500, detail=error_text)
