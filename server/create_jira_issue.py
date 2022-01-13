import json
import os
import requests


def create_issue(issue_summary="Default issue summary, created from python", description_text="default description"):
    # Retrieve the API key secret from the environment
    BASIC = os.environ.get('JIRA_API_BASIC')  # Should be retrieved from google secret manager and injected w/ Helm

    # Prepare the request
    content_type = "application/json"
    url = "https://statistics-norway.atlassian.net/rest/api/3/issue"
    headers = {"Content-Type": content_type, "Authorization": f"Basic {BASIC}"}
    issue_json = get_issue_json(issue_summary=issue_summary, description_text=description_text)

    # Send the issue creation request to Jira
    print("POST new issue")
    r = requests.post(url, headers=headers, data=issue_json)
    print(f"status code {r.status_code} text {r.text}")
    return r.status_code


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


if __name__ == "__main__":
    issue_summary = "Top Text"
    issue_description = f""" bottom 👉👈 text
    
    This issue was created from a Python 🐍 script as a test ✅
    This is a multi-line f-string 🇫🧵 with variables inserted 💉 
    For example, here comes the issue_summary: "{issue_summary}".
    """
    create_issue(issue_summary, issue_description)
