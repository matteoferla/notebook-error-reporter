from .event import ErrorEvent
from .message import ErrorSlack

class ErrorReporter(ErrorSlack, ErrorEvent):
    pass