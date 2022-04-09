import requests, unicodedata, re
from typing import Optional, Union

class ErrorSlack:
    def __init__(self, slack_webhook:Optional[str]):
        # copypasta --> (os.environ['SLACK_WEBHOOK'])
        self.slack_webhook:Union[None, str] = slack_webhook

    def on_error(self, error: Exception, first_line: Optional[str]=None):
        msg = f'{error.__class__.__name__}: {error}'
        if first_line:
            msg += f' in "{first_line}"'
        try:
            if self.slack_webhook:
                self.slack(msg)
        except Exception as sending_error:
            print(f'Awkward turtle! Could not send the message {msg},' +
                  f'reason: {sending_error.__class__.__name__}: {sending_error}')

    def slack(self, msg: str):
        msg = "".join(ch for ch in msg if unicodedata.category(ch)[0] != "C")  # control characters make web sad
        msg = unicodedata.normalize('NFKD', msg).encode('ascii', 'ignore').decode('ascii')  # I [] Unicode
        response = requests.post(url=self.slack_webhook,
                                 headers={'Content-type': 'application/json'},
                                 data=f"{{'text': '{msg}'}}")
        response.raise_for_status()
