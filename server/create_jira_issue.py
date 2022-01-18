import json
import os
from typing import List, Optional
import requests
from pydantic import BaseModel


class ProjectDetails(BaseModel):
    display_team_name: str
    uniform_team_name: str
    manager_email_list: List[str]
    dpo_email_list: Optional[List[str]]
    dev_email_list: Optional[List[str]]
    consumer_email_list: Optional[List[str]]
    service_list: Optional[List[str]]


def create_dapla_start_issue(details: ProjectDetails):
    issue_summary, description_text = get_issue_description(details)
    return create_issue(issue_summary, description_text)


def create_issue(issue_summary, description_text):
    # Retrieve the API key secret from the environment
    basic = os.environ.get('JIRA_API_BASIC')
    if basic is None or len(basic) == 0:
        print('ABORTING! The env variable JIRA_API_BASIC must be set to be your base64 encoded "email:APIkey" string.')
        exit(1)

    # Prepare the request
    content_type = "application/json"
    url = "https://statistics-norway.atlassian.net/rest/api/3/issue"
    headers = {"Content-Type": content_type, "Authorization": f"Basic {basic}"}
    issue_json = get_issue_json(issue_summary=issue_summary, description_text=description_text)

    # Send the issue creation request to Jira
    print("POST new issue")
    r = requests.post(url, headers=headers, data=issue_json)
    print(f"status code {r.status_code} text {r.text}")
    return r


def get_issue_json(issue_summary="Default issue summary, created from python", description_text="default description"):
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
    return json.dumps(issue_dict)


def get_issue_description(details: ProjectDetails):
    """
    This function generates the issue description which contains all the information needed in order to complete
    the creation of a Dapla team
    :param details: Contains all required information
    :return: The summary and complete issue description containing all information needed to create a Dapla team
    """
    summary = f"On-boarding: {details.display_team_name}"  # This is the "header" of the Jira issue
    iac_git_project_name = f"dapla-team-{details.uniform_team_name}"
    domain = "@groups.ssb.no"
    mgm_group = f"{details.uniform_team_name}-managers{domain}"
    dpo_group = f"{details.uniform_team_name}-data-protection-officers{domain}"
    dev_group = f"{details.uniform_team_name}-developers{domain}"
    con_group = f"{details.uniform_team_name}-consumers{domain}"

    # The body of the jira issue
    description = f"""Display team name: '{details.display_team_name}'
    Team name: '{details.uniform_team_name}'
    IAC GIT project name: '{iac_git_project_name}'
    
    ** 1. AD group creation  **
    These AD groups should be created for the team. It's fastest to ask Magnus Myrdal Jenssen, 
    but kundeservice@ssb.no can also do it if he is away.
    
    Managers:
        AD group: {mgm_group}
        members: {details.manager_email_list}
        
    Data Protection Officers:
        AD group: {dpo_group}
        members: {details.dpo_email_list}
        
    Developers:
        AD group: {dev_group}
        members: {details.dev_email_list}
        
    Consumers:
        AD group: {con_group}
        members: {details.consumer_email_list}
        
    
    ** 2. bip-gcp-base-config **
    AFTER AD groups have been created, add the following line:
    "{details.uniform_team_name}" : "{mgm_group}
    
    ...to the dictionary in this file: 
    https://github.com/statisticsnorway/bip-gcp-base-config/blob/main/terraform.tfvars
 
 
    ** 3. Create GCP Team IAC GIT repository **
    IAC GIT project name: '{iac_git_project_name}'
    dapla-start has support for iac git repo creation using terraform templates. Now would be the time to use it!
    
    There should probably be a dump of all the info needed for the github project here:
    
    
    ** 4. Atlantis Whitelist **
    Once the IAC git repository has been created, it needs to be whitelisted by BIP Atlantis. 
    
    Hei Stratus, kan dere Atlantis-whiteliste repoet '{iac_git_project_name}'?
    
    
    ** 5. Apply terraform with Atlantis **
    Create a pull request in '{iac_git_project_name}' 
    and run the "Atlantis apply" command in the pull request before you merge and delete the branch.
    This will cause Atlantis to build our requested infrastructure in GCP.
 
 
    ** 6. Additional Services **
    Requested services: {details.service_list}
    
    If transfer service is requested, send a request to Kundeservice. 
    Kundeservice needs to set up the transfer service agent and directory in linuxstammen.
    
    '''
    Hei Kundeservice,
    
    Det nye dapla teamet '{details.display_team_name}' ({details.uniform_team_name}) trenger transfer service satt opp for seg.
    
    Teamets leder(e): {details.manager_email_list}
        AD-gruppe: {mgm_group}
        
    Teamets dataadministrator(er): {details.dpo_email_list}
        AD-gruppe: {mgm_group}
    
    Fint om dere kan ordne det!
    
    Vennlig hilsen,
    '''
    
    After kundeservice has activated the agent and created the directory structure in linuxstammen, 
    you can refer the managers ({details.manager_email_list}) and/or DPOs ({details.dpo_email_list}) to the docs
    for activating the transfer service on the GCP side:
    
    https://docs.dapla.ssb.no/dapla-user/transfer/
    
    ** Done! **
    
    Congratulations, if everything went according to plan, you are now done!
    
    """
    return summary, description


def generic_issue_creation_test():
    issue_summary = "Top Text"
    issue_description = f""" bottom 👉👈 text
    
    This issue was created from a Python 🐍 script as a test ✅
    This is a multi-line f-string 🇫🧵 with variables inserted 💉 
    For example, here comes the issue_summary: "{issue_summary}".
    """
    authentication_env_var = 'JIRA_API_BASIC'
    basic = os.environ.get(authentication_env_var)
    if basic is None or len(basic) == 0:
        os.environ[authentication_env_var] = ""  # insert base64 encoded "email:key" here
        basic = os.environ.get(authentication_env_var)
        if basic is None or len(basic) == 0:
            print(f'The env variable {authentication_env_var} must be set to be a base64 encoded "email:key" string')
            exit(1)

    create_issue(issue_summary, issue_description)


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
            print(f'The env variable {authentication_env_var} must be set to be a base64 encoded "email:key" string')
            exit(1)

    # Team info
    det_dict = {
        "display_team_name": "Team Domene Subdomene",
        "uniform_team_name": "domene-subdomene",
        "manager_email_list": ["erv@ssb.no"],
        "dpo_email_list": ["mmj@ssb.no"],
        "dev_email_list": ["old@ssb.no", "xyz@ssb.no"],
        "consumer_email_list": ["abc@ssb.no", "def@ssb.no"],
        "service_list": ["transfer service"]
    }
    project_details = ProjectDetails.parse_obj(det_dict)

    minimal_det_dict = {
        "display_team_name": "Team Minimal",
        "uniform_team_name": "minimal",
        "manager_email_list": ["min@ssb.no"]
    }
    min_project_details = ProjectDetails.parse_obj(minimal_det_dict)

    # Creation
    create_dapla_start_issue(min_project_details)
