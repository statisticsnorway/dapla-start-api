from typing import List, Optional

from pydantic import BaseModel


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
