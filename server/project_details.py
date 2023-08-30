from typing import List, Optional
from pydantic import BaseModel
import jwt


class ProjectUser(BaseModel):
    name: str
    email_short: str
    email: str


class OrganizationInfo(BaseModel):
    code: str
    name: str
    parent_code: str


class ProjectDetails(BaseModel):
    display_team_name: str
    uniform_team_name: Optional[str] = None
    manager: ProjectUser
    data_admins: Optional[List[ProjectUser]] = None
    developers: Optional[List[ProjectUser]] = None
    consumers: Optional[List[ProjectUser]] = None
    support: Optional[List[ProjectUser]] = None
    org_info: Optional[OrganizationInfo] = None
    enabled_services: Optional[List[str]] = None
    authorization_code: Optional[str] = None
    reporter: Optional[ProjectUser] = None
    other_info: Optional[str] = None
    ui_version: Optional[str] = None
    api_version: Optional[str] = None


def project_user_from_jwt(token: str):
    decoded = jwt.decode(
        token,
        options={"verify_signature": False, "verify_aud": False, "verify_exp": False},
        algorithms=["HS256", "RS256"],
    )
    email_short = (
        decoded["preferred_username"]
        if "preferred_username" in decoded
        else decoded["email"]
    )
    return ProjectUser(
        name=decoded["name"], email=decoded["email"], email_short=email_short
    )
