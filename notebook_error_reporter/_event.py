from IPython.core.interactiveshell import InteractiveShell, ExecutionResult


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

    def load_ipython_extension(self):
        """
        calling this method enables the error messaging by registering `self._post_run_cell`.
        """
        shell: InteractiveShell = get_ipython()  # noqa
        shell.events.register('post_run_cell', self._post_run_cell)

    def on_error(self, *args, **kwargs):
        pass # virtual method to be overridden.


ErrorEvent().load_ipython_extension()
