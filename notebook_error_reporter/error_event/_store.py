# alt class
from typing import Optional, List, Dict, Union
from ._traceback import ErrorTraceback, TracebackDetailsType, EventDetailsType
# key method of `ErrorTraceback` is `get_details(self, error:Exception)  -> EventDetailsType`
from ._event import ErrorEvent
from datetime import datetime


class EventStoreType(EventDetailsType):
    execution_count: int
    first_line: str
    error: Exception
    timestap: datetime


class ErrorStore(ErrorTraceback, ErrorEvent):
    def __init__(self):
        self.error_details: List[EventStoreType] = []

    def on_error(self,
                 error: Exception,
                 execution_count: int,
                 first_line: Optional[str] = None) -> EventStoreType:
        """
        Method that handles the error reporting by
        getting details from `ErrorTraceback.get_details`
        and storing it in `error_details`.

        The details contain two extra keys, `timestamp`,
        because in the sending data routes the server assigns a timestamp.
        and 'error', because it is un json'able.

        :param error: Exception
        :param execution_count: cell execution count
        :param first_line: the first line of a cell assuming the ad hoc convention that it has a title of sorts.
        :return:
        """
        details: EventStoreType = {**self.get_details(error),
                                   'first_line': str(first_line),
                                   'execution_count': int(execution_count),
                                   'timestamp': datetime.now(),
                                   'error': error
                                   }
        self.error_details.append(details)
        return details
