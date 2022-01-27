import requests
import logging
import os


content_type_json = "application/json"


class AbstractClient:
    def __init__(
            self,
            base_url,
    ):
        self._base_url = base_url.rstrip('/')


class JiraClient(AbstractClient):

    def create_issue(self, json):
        url = self._base_url + "/issue"
        logging.info(f"Calling endpoint:{url}")
        response = requests.post(url, headers=self.create_headers(), json=json)
        response.raise_for_status()
        return response.json()

    def create_headers(self):
        # Retrieve the API key secret from the environment
        basic = os.environ.get('JIRA_API_BASIC')

        if basic is None or len(basic) == 0:
            logging.error(
                'ABORTING! The env variable JIRA_API_BASIC must be set to be your base64 encoded "email:APIkey" string.'
            )
            raise Exception('Missing env variable JIRA_API_BASIC')
        return {"Content-Type": content_type_json, "Authorization": f"Basic {basic}"}



