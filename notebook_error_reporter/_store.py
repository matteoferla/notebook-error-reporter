# alt class
from typing import Optional, List, Dict, Union
from ._traceback import ErrorTraceback, TracebackDetailsType
# key method of `ErrorTraceback` is `get_details(self, error:Exception) \
# -> Dict[str, Union[str, List[TracebackDetailsType]]]`
from ._event import ErrorEvent
from datetime import datetime


class ErrorStore(ErrorTraceback, ErrorEvent):
    def __init__(self):
        self.error_details: List = []

    def on_error(self,
                 error: Exception,
                 execution_count: int,
                 first_line: Optional[str] = None):
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
        details: Dict[str, Union[int, str, datetime, Exception, List[TracebackDetailsType]]] = self.get_details(error)
        details['first_line']: str = first_line
        details['execution_count']: int = int(execution_count)
        details['timestamp'] = datetime.now()
        details['error']: Exception = error
        self.error_details.append(details)
