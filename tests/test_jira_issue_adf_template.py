from tests import resolve_filename
from server.jira_issue_adf_template import _description
from server.project_details import ProjectDetails, ProjectUser
import json


def test_create_issue():
    project_details = ProjectDetails(
        display_team_name="Team Stubbe",
        manager=ProjectUser(name="Magnus Manager", email="mm@ssb.no"),
        data_protection_officers=[ProjectUser(name="Pernille Pilot", email="ppi@ssb.no"),
                                  ProjectUser(name="Petter Andrepilot ", email="pap@ssb.no")],
        developers=[ProjectUser(name="Dorte Developer", email="dd@ssb.no"),
                    ProjectUser(name="Diana Developer", email="did@ssb.no")],
        reporter=ProjectUser(name="Reidar Reporter", email="rr@ssb.no")
    )
    with open(resolve_filename("adf_template_result.json"), encoding="utf-8") as file:
        assert json.dumps(_description(project_details), indent=2, ensure_ascii=False) == file.read()
