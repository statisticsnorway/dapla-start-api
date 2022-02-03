from typing import List, Optional
from pydantic import BaseModel
import jwt


class ProjectUser(BaseModel):
    name: str
    email_short: str
    email: str


class ProjectDetails(BaseModel):
    display_team_name: str
    manager: ProjectUser
    data_protection_officers: Optional[List[ProjectUser]]
    developers: Optional[List[ProjectUser]]
    consumers: Optional[List[ProjectUser]]
    enabled_services: Optional[List[str]]
    authorization_code: Optional[str]
    reporter: Optional[ProjectUser]
    other_info: Optional[str]
    ui_version: Optional[str]
    api_version: Optional[str]


def project_user_from_jwt(token: str):
    decoded = jwt.decode(token, options={
        "verify_signature": False,
        "verify_aud": False,
        "verify_exp": False
    }, algorithms=["HS256", "RS256"])
    email_short = decoded['preferred_username'] if 'preferred_username' in decoded else decoded['email']
    return ProjectUser(name=decoded['name'], email=decoded['email'], email_short=email_short)
