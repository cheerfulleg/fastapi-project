from typing import Optional

from pydantic import BaseModel


class CeleryBody(BaseModel):
    type: int = 1


class TaskStatus(BaseModel):
    task_id: str
    task_status: str
    task_result: Optional[bool] = None
