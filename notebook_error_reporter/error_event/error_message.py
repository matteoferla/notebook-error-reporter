import json
import warnings
import requests, unicodedata, re
from typing import Optional, Union, Dict, List

from ._traceback import ErrorTraceback, TracebackDetailsType, EventDetailsType


class EventMessageType(EventDetailsType):
    notebook: str
    execution_count: int
    first_line: str

# key method of `ErrorTraceback` is `get_details(self, error:Exception)  -> EventDetailsType`
from .error_event import ErrorEvent


class ErrorSlack(ErrorTraceback, ErrorEvent):
    def __init__(self, notebook: str='unknown', slack_webhook: Optional[str] = None):
        # copypasta --> (os.environ['SLACK_WEBHOOK'])
        self.slack_webhook: Union[None, str] = slack_webhook
        self.notebook = notebook

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
                                     'execution_count': int(execution_count),
                                     'notebook': self.notebook
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

class ErrorServer(ErrorTraceback, ErrorEvent):
    def __init__(self, url: str, notebook: str='unknown'):
        self.url: str = url
        self.notebook = notebook
        response = requests.post(f'{url}/usages/',
                                 json={'notebook': self.notebook})
        response.raise_for_status()
        self.uuid:str = response.json()['uuid']

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
                                     'execution_count': int(execution_count),
                                     'notebook': self.notebook
                                     }
        response = requests.post(f'{self.url}/errors/{self.uuid}',
                                 json=details)
        if response.status_code != 200:
            warnings.warn(f'Additionally there was an error reporting failure: {response.json()}')

    def retrieve_errors(self) -> List[EventMessageType]:
        response = requests.get(f'{self.url}/usages/{self.uuid}')
        response.raise_for_status()
        return response.json()

