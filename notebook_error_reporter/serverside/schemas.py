from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

class ErrorBase(BaseModel):
    name: str
    message: Optional[str] = None
    traceback: List[dict] = []


class ErrorCreate(ErrorBase):
    pass


class Error(ErrorBase):
    id: int
    usage_uuid: str
    time: datetime

    class Config:
        orm_mode = True

# ===========================================================================

class UsageBase(BaseModel):
    notebook: str


class UsageCreate(UsageBase):
    pass


class Usage(UsageBase):
    id: int
    ip: str
    uuid: str
    time: datetime
    errors: List[Error] = []

    class Config:
        orm_mode = True
