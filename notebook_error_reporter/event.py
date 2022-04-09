from IPython.core.interactiveshell import InteractiveShell, ExecutionResult


class ErrorEvent:
    def post_run_cell(self, result: ExecutionResult):
        """
        This is called after the cell is run and if an error occured calls `on_error`.

        :param result: the output of InteractiveShell.run_code
        :return: None
        """
        if hasattr(result, 'error_in_exec') and result.error_in_exec is not None:

            self.on_error(error=result.error_in_exec,
                          first_line=result.info.raw_cell.split('\n')[0])

    def load_ipython_extension(self):
        shell: InteractiveShell = get_ipython()  # noqa
        shell.events.register('post_run_cell', self.post_run_cell)

    def on_error(self, error: Exception):
        raise NotImplementedError('virtual method')


ErrorEvent().load_ipython_extension()
