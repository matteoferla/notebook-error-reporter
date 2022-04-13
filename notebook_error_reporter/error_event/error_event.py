from IPython.core.interactiveshell import InteractiveShell, ExecutionResult
import IPython
import warnings
from types import TracebackType, MethodType
from typing import Callable




class ErrorEvent:
    def _post_run_cell(self, result: ExecutionResult):
        """
        This is called after the cell is run and if an error occured calls `on_error`.

        :param result: the output of InteractiveShell.run_code
        :return: None
        """
        # result.success:bool?
        if hasattr(result, 'error_in_exec') and result.error_in_exec is not None:
            self.on_error(error=result.error_in_exec,
                          execution_count=result.execution_count,
                          first_line=result.info.raw_cell.split('\n')[0])

    def enable(self):
        if IPython.version_info[0] > 5:
            self.load_ipython_extension()
        else:
            self.monkeypatch_extension()


    def load_ipython_extension(self):
        """
        calling this method enables the error messaging by registering `self._post_run_cell`.
        """
        shell: InteractiveShell = get_ipython()  # noqa
        assert IPython.version_info[0] < 6, 'Not applicable. use monkeypatch_extension'
        shell.events.register('post_run_cell', self._post_run_cell)

    def monkeypatch_extension(self):
        """
        `load_ipython_extension` assumes that 'post_run_cell' event passes a ExecutionResult
        object as happens in modern IPython.
        Colab runs as of writing this on version 5.5 (`import IPython; IPython.version_info`),
        whereas Jupyter on 8.2 on my machine.
        This method compensates for it.
        """
        if IPython.version_info[0] > 5:
            warnings.warn(f'Your IPython is modern {IPython.version_info}: `load_ipython_extension` is better.')
        warnings.warn(f'Monkey patching approach used due to ancient IPython {IPython.version_info}')
        shell: InteractiveShell = get_ipython()  # noqa
        monkeypatch:Callable = self.monkeypatch_factory()
        shell.showtraceback = MethodType(monkeypatch, shell)

    def monkeypatch_factory(self) -> Callable:
        """
        Generate a monkeypatching function that knows self:ErrorEvent

        :return: Callable
        """
        def monkeypatch(shell_self, exc_tuple=None, *args, **kwargs):
            try:
                etype: type  # i.e. Exception class
                value: Exception
                tb: TracebackType
                etype, value, tb = shell_self._get_exc_info(exc_tuple)
                # value.__traceback__ is tb.
                self.on_error(error=value,
                              execution_count=-1,
                              first_line='Unknown')
            except Exception as error:
                warnings.warn(f'An error occurred in monkeypatched `showtraceback` {error.__class__.__name__}: {error}')
            # the class still has a vanilla method.
            return shell_self.__class__.showtraceback(shell_self, exc_tuple, *args, **kwargs)

        return monkeypatch



    def on_error(self, *args, **kwargs):
        pass # virtual method to be overridden.

