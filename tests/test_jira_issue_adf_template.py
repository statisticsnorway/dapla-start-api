from tests import resolve_filename
from server.jira_issue_adf_template import _description
from server.project_details import ProjectDetails, ProjectUser
import json


def test_create_issue():
    project_details = ProjectDetails(
        display_team_name="Team Stubbe",
        manager=ProjectUser(name="Magnus Manager", email_short="mm@ssb.no", email="magnus.manager@ssb.no"),
        data_protection_officers=[ProjectUser(name="Pernille Pilot", email_short="ppi@ssb.no", email="ppi@ssb.no"),
                                  ProjectUser(name="Petter Andrepilot ", email_short="pap@ssb.no", email="pap@ssb.no")],
        developers=[ProjectUser(name="Dorte Developer", email_short="dd@ssb.no", email="dd@ssb.no"),
                    ProjectUser(name="Diana Developer", email_short="did@ssb.no", email="did@ssb.no")],
        reporter=ProjectUser(name="Reidar Reporter", email_short="rr@ssb.no", email="rr@ssb.no")
    )
    with open(resolve_filename("adf_template_result.json"), encoding="utf-8") as file:
        assert json.dumps(_description(project_details), indent=2, ensure_ascii=False) == file.read()
