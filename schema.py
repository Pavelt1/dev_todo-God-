from datetime import datetime,date
from pydantic import BaseModel

class TodoRequest(BaseModel):
    title: str
    description: str
    deadline: date | None
    tags: str | None

class TodoResponse(TodoRequest):
    status: bool
    create_datetime: datetime

class TodoUpdate(BaseModel):
    title: str | None
    description: str | None
    deadline: date | None
    tags: str | None
    status: bool | None