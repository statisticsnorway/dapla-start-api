import json
import os

import requests

from server.jira_issue_adf_template import get_issue_adf_dict
from .project_details import ProjectDetails, ProjectUser
from .config import logger

content_type_json = "application/json"


def create_dapla_start_issue(details: ProjectDetails):
    return create_jira_issue_3lo(details)


def create_issue_basic(details: ProjectDetails):
    return get_issue_adf_dict(details)


def get_authorization_url(state, client_id="3mvYlLJX466VodaubZTD0WcpOSHOnAqa"):
    url_string = (f"https://auth.atlassian.com/authorize"
                  f"?audience=api.atlassian.com"
                  f"&client_id={client_id}"
                  f"&scope=write%3Aissue%3Ajira%20read%3Aproject%3Ajira%20write%3Acomment.property%3Ajira%20write%3Acomment%3Ajira%20write%3Aattachment%3Ajira%20read%3Aissue%3Ajira"
                  f"&redirect_uri=https%3A%2F%2Fstart.dapla.ssb.no%2F2"
                  f"&response_type=code"
                  f"&prompt=consent"
                  f"&state=${state}")  # (required for security) Set this to a value that is associated with the user you are directing to the authorization URL, for example, a hash of the user's session ID.
    """
    If successful, the user will be redirected to the app's callback URL,
    with an authorization code provided as a query parameter called code.
    This code can be exchanged for an access token, as described in step 2.
    State (user bound value) will be preserved.
    """
    return url_string


def get_access_token(authorization_code, client_id="3mvYlLJX466VodaubZTD0WcpOSHOnAqa",
                     callback_url="https://start.dapla.ssb.no/2"):
    atlassian_oauth_token_url = "https://auth.atlassian.com/oauth/token"
    client_secret = os.getenv("OAUTH_2_CLIENT_SECRET")

    if client_secret is None or client_secret == "":
        raise EnvironmentError("OAUTH_2_CLIENT_SECRET was not present in environment!")
    else:
        logger.info("oauth2 client secret variable was present in env")

    headers = {"Content-Type": content_type_json}
    data = {"grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": authorization_code,
            "redirect_uri": callback_url}
    r = requests.post(atlassian_oauth_token_url, headers=headers, data=json.dumps(data))

    return r


def get_cloud_id(access_token):
    """
    The cloud id is an identifier for the jira cloud project that you are trying to hit with the api.
    """
    accessible_resources_url = "https://api.atlassian.com/oauth/token/accessible-resources"
    headers = {"Authorization": f"Bearer {access_token}"}
    accessible_resources_response = requests.get(url=accessible_resources_url, headers=headers)
    data_dict = json.loads(accessible_resources_response.text)
    logger.debug("accessible_resources_response as data dictionary")
    logger.debug(data_dict)
    cloud_id = data_dict[0]["id"]

    return cloud_id


def create_jira_issue_3lo(details, client_id="3mvYlLJX466VodaubZTD0WcpOSHOnAqa",
                          callback_url="https://start.dapla.ssb.no/2", api="/rest/api/3/issue"):
    """
    :param details: Must contain the authorization_code optional field! This can be retrieved from the auth step.
    :param client_id:
    :param callback_url:
    :param api:
    :return:
    """

    logger.debug(f"jira issue creation 3LO method started...")
    get_access_token_response = get_access_token(details.authorization_code, client_id, callback_url)

    if get_access_token_response.status_code != 200:
        raise Exception(f"Access token request returned non-200 status code. Response: {get_access_token_response}")
    logger.debug("access token retrieved with status 200")

    response_dict = json.loads(get_access_token_response.text)
    access_token = response_dict["access_token"]
    response_dict["access_token"] = "REDACTED"
    logger.debug(f"access token response dict: {response_dict}")
    cloud_id = get_cloud_id(access_token)  # id for statistics-norway should be bdafa676-276d-441e-a450-26547c4959cf
    logger.debug(f"organization cloud id: {cloud_id}")
    final_jira_api_post_url = f"https://api.atlassian.com/ex/jira/{cloud_id}{api}"
    logger.debug(f"final jira cloud oauth2 api post url: {final_jira_api_post_url}")
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": content_type_json}

    issue_dict = get_issue_adf_dict(details)

    logger.debug(f"issue dictionary: {issue_dict}")
    logger.debug(f"posting issue json to jira")
    response = requests.post(url=final_jira_api_post_url, headers=headers, data=json.dumps(issue_dict))

    if response.status_code != 201:
        raise Exception(f"[ERROR] Jira issue was not created by post request to jira! "
                        f"Response: {response} Text: {response.text}")

    return response


if __name__ == "__main__":
    """
    This main is for the purposes of testing the jira issue creation functionality.
    """
    
    # Basic auth
    authentication_env_var = 'JIRA_API_BASIC'
    basic = os.environ.get(authentication_env_var)

    encoded_string = base64.b64encode("xxx@ssb.no:abcdefghij".encode()).decode()
    os.environ['JIRA_API_BASIC'] = encoded_string

    if basic is None or len(basic) == 0:
        os.environ[authentication_env_var] = ""  # insert base64 encoded "email:key" here
        basic = os.environ.get(authentication_env_var)

        if basic is None or len(basic) == 0:
            logger.error(
                f'The env variable {authentication_env_var} must be set to be a base64 encoded "email:key" string')
            exit(1)

    # Team info
    xxx_mail_1 = "xxx@ssb.no"
    xxx_mail_2 = "xxx@ssb.no"

    xxx_user_1 = ProjectUser(name="Testbruker 1", email_short=xxx_mail_1, email="xx1@ssb.no")
    xxx_user_2 = ProjectUser(name="Testbruker 2", email_short=xxx_mail_2, email="xx2@ssb.no")


    det_dict = {
        "display_team_name": "Team Domene Subdomene",
        "manager": xxx_user_1,
        "data_admins": [xxx_user_1, xxx_user_2],
        "developers": [xxx_user_1, xxx_user_2],
        "consumers": [xxx_user_1, xxx_user_2],
        "enabled_services": ["transfer service"]
    }
    project_details = ProjectDetails.parse_obj(det_dict)

    minimal_det_dict = {
        "display_team_name": "Team Minimal",
        "manager": xxx_user_1
    }
    min_project_details = ProjectDetails.parse_obj(minimal_det_dict)

    # Creation
    create_dapla_start_issue(min_project_details)
