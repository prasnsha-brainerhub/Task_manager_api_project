from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    pass

    class Config:
        orm_mode = True

