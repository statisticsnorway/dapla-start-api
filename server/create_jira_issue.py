import json
import logging
import os
from typing import List, Optional

import requests
import yaml
from pydantic import BaseModel

content_type_json = "application/json"


class ProjectDetails(BaseModel):
    display_team_name: str
    manager: str
    data_protection_officers: Optional[List[str]]
    developers: Optional[List[str]]
    consumers: Optional[List[str]]
    enabled_services: Optional[List[str]]
    authorization_code: Optional[str]


def create_dapla_start_issue(details: ProjectDetails):
    return create_jira_issue_3lo(details)


def create_issue_basic(details: ProjectDetails):
    issue_summary, description_text = get_issue_description(details)
    # Retrieve the API key secret from the environment
    basic = os.environ.get('JIRA_API_BASIC')

    if basic is None or len(basic) == 0:
        logging.error(
            'ABORTING! The env variable JIRA_API_BASIC must be set to be your base64 encoded "email:APIkey" string.'
        )
        exit(1)

    # Prepare the request
    url = "https://statistics-norway.atlassian.net/rest/api/3/issue"
    headers = {"Content-Type": content_type_json, "Authorization": f"Basic {basic}"}
    issue_dict = get_issue_dict(issue_summary=issue_summary, description_text=description_text)
    # Send the issue creation request to Jira
    r = requests.post(url, headers=headers, data=json.dumps(issue_dict))

    return r


def get_issue_dict(issue_summary="Default issue summary, created from python", description_text="default description"):
    issue_dict = {
        "fields": {
            "project": {
                "key": "DS"  # DS is the 'key' for the Dapla Start project
            },
            "summary": issue_summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": description_text,
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
    }
    return issue_dict


def convert_display_name_to_uniform_team_name(display_team_name):
    return display_team_name.lower().replace("team ", "").replace(" ", "-").replace("æ", "ae").replace("ø",
                                                                                                       "oe").replace(
        "å", "aa")


def get_issue_description(details: ProjectDetails):
    """
    This function generates the issue description which contains all the information needed in order to complete
    the creation of a Dapla team
    :param details: Contains all required information
    :return: The summary and complete issue description containing all information needed to create a Dapla team
    """
    summary = f"On-boarding: {details.display_team_name}"  # This is the "header" of the Jira issue
    uniform_team_name = convert_display_name_to_uniform_team_name(details.display_team_name)
    iac_git_project_name = f"dapla-team-{uniform_team_name}"
    domain = "@groups.ssb.no"
    mgm_group = f"{uniform_team_name}-managers{domain}"
    dpo_group = f"{uniform_team_name}-data-protection-officers{domain}"
    dev_group = f"{uniform_team_name}-developers{domain}"
    con_group = f"{uniform_team_name}-consumers{domain}"
    services_dict = {"display_team_name": details.display_team_name}

    if details.enabled_services and isinstance(details.enabled_services, list):
        for service in details.enabled_services:
            services_dict[f"enable_{service}"] = 'yes'

    # The body of the jira issue
    description = f"""\
YAML:
```
{yaml.dump(services_dict)}
```

Uniform team name: '{uniform_team_name}'
IaC GitHub project name: '{iac_git_project_name}'

** 1. AD group creation  **
These AD groups should be created for the team. Send the request to kundeservice@ssb.no.

Managers:
    AD group: {mgm_group}
    members: {details.manager}
    
Data Protection Officers:
    AD group: {dpo_group}
    members: {details.data_protection_officers}
    
Developers:
    AD group: {dev_group}
    members: {details.developers}
    
Consumers:
    AD group: {con_group}
    members: {details.consumers}
    

** 2. bip-gcp-base-config **
AFTER AD groups have been created, add the following line:
"{uniform_team_name}" : "{mgm_group}"

...to the dictionary in this file: 
https://github.com/statisticsnorway/bip-gcp-base-config/blob/main/terraform.tfvars


** 3. Create GCP Team IaC GitHub repository **
IaC GitHub project name: '{iac_git_project_name}'

Use the dapla-start-toolkit for this.


** 4. Atlantis Whitelist **
Once the IaC GitHub repository has been created, it needs to be whitelisted by BIP Atlantis. 

Hei Stratus, kan dere whiteliste repoet '{iac_git_project_name}' i Atlantis?


** 5. Apply terraform with Atlantis **
Create a pull request in '{iac_git_project_name}', get approval from Team Stratus
and then run the "Atlantis apply" command in the pull request before you merge and delete the branch.
This will cause Atlantis to build our requested infrastructure in GCP.


** 6. Additional Services **
Requested services: {details.enabled_services}

If Transfer Service is requested, send a request to Kundeservice. 
Kundeservice needs to set up the Transfer Service agent and directory in Linuxstammen.

'''
Hei Kundeservice,

Det nye dapla teamet '{details.display_team_name}' trenger transfer service satt opp for seg.

AD-gruppe som skal ha tilgang til synk område on-prem:
    {dpo_group}

Prosjektnavn i GCP
    {uniform_team_name}-ts

Fint om dere kan ordne det!

Vennlig hilsen,
'''

After Kundeservice has activated the agent and created the directory structure in Linuxstammen, 
you can refer the managers ({details.manager}) and/or DPOs ({details.data_protection_officers}) to the docs
for activating the transfer service on the GCP side:

https://docs.dapla.ssb.no/dapla-user/transfer/

** Done! **

Congratulations, if everything went according to plan, you are now done!

"""

    return summary, description


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
        logging.info("oauth2 client secret variable was present in env")

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
    logging.debug("accessible_resources_response as data dictionary")
    logging.debug(data_dict)
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

    logging.debug(f"jira issue creation 3LO method started...")
    issue_summary, description_text = get_issue_description(details)
    get_access_token_response = get_access_token(details.authorization_code, client_id, callback_url)

    if get_access_token_response.status_code != 200:
        raise Exception(f"Access token request returned non-200 status code. Response: {get_access_token_response}")
    logging.debug("access token retrieved with status 200")

    response_dict = json.loads(get_access_token_response.text)
    access_token = response_dict["access_token"]
    response_dict["access_token"] = "REDACTED"
    logging.debug(f"access token response dict: {response_dict}")
    cloud_id = get_cloud_id(access_token)  # id for statistics-norway should be bdafa676-276d-441e-a450-26547c4959cf
    logging.debug(f"organization cloud id: {cloud_id}")
    final_jira_api_post_url = f"https://api.atlassian.com/ex/jira/{cloud_id}{api}"
    logging.debug(f"final jira cloud oauth2 api post url: {final_jira_api_post_url}")
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": content_type_json}
    issue_dict = get_issue_dict(issue_summary=issue_summary, description_text=description_text)
    logging.debug(f"issue dictionary: {issue_dict}")
    logging.debug(f"posting issue json to jira")
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

    if basic is None or len(basic) == 0:
        os.environ[authentication_env_var] = ""  # insert base64 encoded "email:key" here
        basic = os.environ.get(authentication_env_var)

        if basic is None or len(basic) == 0:
            logging.error(
                f'The env variable {authentication_env_var} must be set to be a base64 encoded "email:key" string')
            exit(1)

    # Team info
    xxx_mail = "xxx@ssb.no"
    det_dict = {
        "display_team_name": "Team Domene Subdomene",
        "manager": xxx_mail,
        "data_protection-officers": [xxx_mail],
        "developers": [xxx_mail, xxx_mail],
        "consumers": [xxx_mail, xxx_mail],
        "enabled_services": ["transfer service"]
    }
    project_details = ProjectDetails.parse_obj(det_dict)

    minimal_det_dict = {
        "display_team_name": "Team Minimal",
        "manager": xxx_mail
    }
    min_project_details = ProjectDetails.parse_obj(minimal_det_dict)

    # Creation
    create_dapla_start_issue(min_project_details)
