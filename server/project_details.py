from pydantic import BaseModel
from typing import List, Optional


class ProjectDetails(BaseModel):
    display_team_name: str
    manager: str
    data_protection_officers: Optional[List[str]]
    developers: Optional[List[str]]
    consumers: Optional[List[str]]
    enabled_services: Optional[List[str]]
    authorization_code: Optional[str]
