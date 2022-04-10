from typing import Sequence, List, Tuple, Union, Dict
import sys

if sys.version_info < (3, 8):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict
from types import TracebackType
import site


class TracebackDetailsType(TypedDict):
    filename: str
    fun_name: str
    lineno: int


class EventDetailsType(TypedDict):
    error_name: str
    error_message: str
    traceback: List[TracebackDetailsType]


class ErrorTraceback:
    def get_details(self, error: Exception) -> EventDetailsType:
        """
        Given an error return a dictionary of keys 'error_name' (str), 'error_message' (str)
        and traceback, which is a partial misnomer as its value is not a `TracebackType`,
        but a list of dict with keys 'filename', 'fun_name', 'lineno'.

        'filename' is trimmed down for privacy concerns:

        The `dist-packages` path in colab should be
         `/usr/local/lib/python3.7/dist-packages/rdkit_to_params/__init__.py`,
         but it may be a local jupyter notebook in a Conda environment:
         `/Users/matteoferla/[...]/rdkit_to_params/__init__.py`
         The username _could_ have personal identifiable information,
         So it needs stripping of the dist-packages path.
        """
        traceback: Union[TracebackType, None] = error.__traceback__
        details = []
        if traceback is not None:
            details = [self._get_single_traceback_details(traceback)]
            traceback: TracebackType = traceback.tb_next
            while traceback is not None:
                details.append(self._get_single_traceback_details(traceback))
                traceback: Union[TracebackType, None] = traceback.tb_next
        return dict(error_name=error.__class__.__name__,
                    error_message=str(error),
                    traceback=details)

    def _get_single_traceback_details(self, traceback: TracebackType) -> TracebackDetailsType:
        """
        Returns the details of a given traceback object,
        but trims the filename as discussed in `get_details`.

        :param traceback:
        :return: dict filename, fun_name, lineno
        """
        # strip the `dist-packages` path in case it has PID.
        filename: str = traceback.tb_frame.f_code.co_filename
        for path in site.getsitepackages():
            filename = filename.replace(path, '')
        # return the filename, fun name and line
        return dict(filename=filename,
                    fun_name=traceback.tb_frame.f_code.co_name,
                    lineno=traceback.tb_lineno)
