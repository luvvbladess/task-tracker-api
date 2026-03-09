from typing import Optional, List
from pydantic import BaseModel


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagInDBBase(TagBase):
    id: int

    model_config = {"from_attributes": True}


class Tag(TagInDBBase):
    pass


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    project_id: int
    assignee_id: Optional[int] = None


class TaskCreate(TaskBase):
    tags: Optional[List[str]] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None
    tags: Optional[List[str]] = None


class TaskInDBBase(TaskBase):
    id: int
    tags: List[Tag] = []

    model_config = {"from_attributes": True}


class Task(TaskInDBBase):
    pass
