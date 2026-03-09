from typing import Optional
from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class ProjectInDBBase(ProjectBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}

class Project(ProjectInDBBase):
    pass
