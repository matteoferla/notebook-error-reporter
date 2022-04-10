from typing import List, Optional
from datetime import datetime

# from .error_event import EventMessageType
# ref for eventMessageType
# class TracebackDetailsType(TypedDict):
#     filename: str
#     fun_name: str
#     lineno: int
#
# class EventMessageType:
#     error_name: str
#     error_message: str
#     traceback: List[TracebackDetailsType]
#     execution_count: int
#     first_line: str

from pydantic import BaseModel

class ErrorBase(BaseModel):
    error_name: str
    error_message: Optional[str] = None
    traceback: List[dict] = []
    execution_count: int
    first_line: str


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
