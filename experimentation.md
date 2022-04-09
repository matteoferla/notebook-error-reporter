## Magic

I had assumed a cell magic that run the cell block within a try-catch would be fine:
```python
from IPython.core.magic import  ( Magics, magics_class, cell_magic )
from IPython.core.interactiveshell import InteractiveShell, ExecutionResult

@magics_class
class ErrorReporter(Magics):
    # run the cell as a global, so no @needs_local_scope
    @cell_magic
    def error_reporter(self, line, cell):
        """Take note of errors"""
        #exec(cell, None, local_ns)
        shell:InteractiveShell = get_ipython()  # noqa `get_ipython` is present in notebooks
        try:
            result:ExecutionResult = shell.run_cell(cell)
        except Exception as error:
            print(type(error))
        return None # behave like a normal cell: the `run_cell` will display the `_`.

shell:InteractiveShell = get_ipython() # noqa `get_ipython` is present in notebooks
shell.register_magics(ErrorReporter)
```
To be run in a cell like:
```python
%%error_reporter

raise ValueError('Help!')
```

However, this is not the case. Using `capture_output` does not do the trick either.
```python
from IPython.utils.capture import capture_output
from IPython.core.interactiveshell import InteractiveShell, ExecutionResult
cell = 'print("hello world")\nraise ValueError("hello sun")'
shell:InteractiveShell = get_ipython()  # noqa `get_ipython` is present in notebooks
with capture_output(stdout=True, stderr=True, display=True) as captured: #: CapturedIO
    result:ExecutionResult = shell.run_cell(cell)
    print('This will not be run...')
    print(captured.stdout)
    print(captured.stderr)
    print(captured.outputs)
print('This will not be run...')
```
## Monkeypatching showtraceback

Another way is to monkeypatch `InteractiveShell.showtraceback`:

```python
from IPython.core.interactiveshell import InteractiveShell
import inspect

print(inspect.getsource(InteractiveShell.showtraceback))
```

This shows there's a lot of code going on, so instead of a substitution a decorator would be better:

```python

from types import TracebackType
from typing import Tuple

def monkeypatch(self, exc_tuple=None, *args, **kwargs):
        try: 
            etype: type  # i.e. Exception class
            value:Exception
            tb:TracebackType
            etype, value, tb  = self._get_exc_info(exc_tuple)
            print(f'Snap! You just got a {etype}, {value}')
        except Exception:
            pass
        return InteractiveShell.showtraceback(self, exc_tuple, *args, **kwargs)
        

from IPython.core.interactiveshell import InteractiveShell
import types

ishell:InteractiveShell = get_ipython() # noqa
ishell.showtraceback = types.MethodType(monkeypatch, ishell)
```

This works, but may cause trouble...

## Events

Instead, and potentially better is [events](https://ipython.readthedocs.io/en/stable/config/callbacks.html).
However, annoyingly, whereas `'post_run_cell'` accepts a `ExecutionResult`, 
this does not hold a traceback from what I could tell.

```python
from IPython.core.interactiveshell import InteractiveShell, ExecutionResult

def post_run_cell(result: ExecutionResult):
    if hasattr(result, 'error_in_exec') and result.error_in_exec is not None:
        error: Exception = result.error_in_exec
        print(f'You got a {error.__class__.__name__} {error}')
        
def load_ipython_extension(shell: InteractiveShell):
    shell.events.register('post_run_cell', post_run_cell)
    
load_ipython_extension(get_ipython())  # noqa
```
Perfetto!
