from tests import resolve_filename
from server.jira_issue_adf_template import (
    _description,
    convert_display_name_to_uniform_team_name,
)
from server.project_details import ProjectDetails, ProjectUser, OrganizationInfo
import json
import pytest
from jsonschema import validate
import requests
from datetime import date


@pytest.fixture()
def project_details():
    return ProjectDetails(
        display_team_name="Team Stubbe",
        uniform_team_name="stubbs",
        manager=ProjectUser(
            name="Magnus Manager",
            email_short="mm@ssb.no",
            email="magnus.manager@ssb.no",
        ),
        data_admins=[
            ProjectUser(
                name="Pernille Pilot", email_short="ppi@ssb.no", email="ppi@ssb.no"
            ),
            ProjectUser(
                name="Petter Andrepilot ", email_short="pap@ssb.no", email="pap@ssb.no"
            ),
        ],
        developers=[
            ProjectUser(
                name="Dorte Developer", email_short="dd@ssb.no", email="dd@ssb.no"
            ),
            ProjectUser(
                name="Diana Developer", email_short="did@ssb.no", email="did@ssb.no"
            ),
        ],
        org_info=OrganizationInfo(code="11", name="Seksjon 11", parent_code="1"),
        reporter=ProjectUser(
            name="Reidar Reporter", email_short="rr@ssb.no", email="rr@ssb.no"
        ),
        other_info="Some other info",
    )


@pytest.fixture()
def description(project_details):
    return _description(project_details, date.fromisoformat("2022-02-01"))


@pytest.fixture()
def json_schema():
    return requests.get(
        "https://unpkg.com/@atlaskit/adf-schema@latest/dist/json-schema/v1/full.json"
    ).json()


def test_create_issue_valid_json_schema(description, json_schema):
    # Validate against Atlassian Document Format schema
    validate(instance=description, schema=json_schema)


def test_create_issue_generated_dict(description):
    with open(resolve_filename("adf_template_result.json"), encoding="utf-8") as file:
        expected = json.load(file)
    assert len(description["content"]) == len(expected["content"])
    for actual, expected in zip(description["content"], expected["content"]):
        assert actual == expected


def test_create_issue_exact_file_text(description):
    with open(resolve_filename("adf_template_result.json"), encoding="utf-8") as file:
        result = json.dumps(description, indent=2, ensure_ascii=False) + "\n"
        assert result == file.read()


@pytest.mark.parametrize(
    "display,uniform",
    [
        ("Team Stubbe", "stubbe"),
        ("æøå", "aeoeaa"),
        ("ÆØÅ", "aeoeaa"),
    ],
)
def test_convert_display_name_to_uniform_team_name(display, uniform):
    assert uniform == convert_display_name_to_uniform_team_name(display)
