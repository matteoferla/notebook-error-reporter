import json

import requests, unicodedata, re
from typing import Optional, Union, Dict, List

from ._traceback import ErrorTraceback, TracebackDetailsType, EventDetailsType


class EventMessageType(EventDetailsType):
    execution_count: int
    first_line: str

# key method of `ErrorTraceback` is `get_details(self, error:Exception)  -> EventDetailsType`
from ._event import ErrorEvent


class ErrorSlack(ErrorTraceback, ErrorEvent):
    def __init__(self, slack_webhook: Optional[str]):
        # copypasta --> (os.environ['SLACK_WEBHOOK'])
        self.slack_webhook: Union[None, str] = slack_webhook

    def on_error(self,
                 error: Exception,
                 execution_count: int,
                 first_line: str='') -> EventMessageType:
        """
        Method that handles the error reporting by
        getting details from `ErrorTraceback.get_details`
        and setting the via slack (`.send_slack`).

        :param error: Exception
        :param execution_count: cell execution count
        :param first_line: the first line of a cell assuming the ad hoc convention that it has a title of sorts.
        :return:
        """
        details: EventMessageType = {**self.get_details(error),
                                     'first_line': str(first_line),
                                     'execution_count': int(execution_count)
                                     }
        msg = json.dumps(details)
        try:
            if self.slack_webhook:
                self.send_slack(msg)
            else:
                raise NotImplementedError('No alt option set up')
        except Exception as sending_error:
            print(f'Awkward turtle! Could not send the message {msg},' +
                  f'reason: {sending_error.__class__.__name__}: {sending_error}')
        return details

    def send_slack(self, msg: str):
        msg = "".join(ch for ch in msg if unicodedata.category(ch)[0] != "C")  # control characters make web sad
        msg = unicodedata.normalize('NFKD', msg).encode('ascii', 'ignore').decode('ascii')  # I [] Unicode
        response = requests.post(url=self.slack_webhook,
                                 headers={'Content-type': 'application/json'},
                                 data=f"{{'text': '{msg}'}}")
        response.raise_for_status()
