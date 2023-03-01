# author: shiyao
# created: 2021/9/16

import sys
import time 
import datetime
import inspect 
from termcolor import colored
from tool_shack.core import now_str
from collections import deque
from contextlib import contextmanager
import humanize
import colorful
import colour

from typing import Optional, Callable, Tuple, TextIO

class EmptyContext(): 
    '''
    a No-op context manager.

    in case you need to get rid of one of these context managers
    but don't want to bother with the indentation. switch this inplace.
    
    '''
    def __init__(self, *args, **kwargs): 
        pass 
    def __enter__(self): 
        pass 
    def __exit__(self, exec_type, exc_val, exc_tb): 
        pass

class IndentStdout(): 
    def __init__(self, indent_space = 2): 
        self.indent_space = indent_space
        self.indent_level = 0
        self._sys_stdout = sys.stdout

    @property
    def activated(self,) -> bool: return self.indent_level > 0

    def write(self, message):
        indent_str = ' ' * (self.indent_space * self.indent_level)
        self._sys_stdout.write(indent_str + message)
    
    def flush(self, ): 
        self._sys_stdout.flush()
    
    def print_through(self, *args, **kwargs):
        print(*args, **kwargs, file=self._sys_stdout)
    
    def increase(self, ): 
        self.indent_level += 1
        if self.activated: sys.stdout = self
    
    def decrease(self, ): 
        self.indent_level -= 1
        if not self.activated: sys.stdout = self._sys_stdout

_indent_stdout = IndentStdout()

class StageLogger(): 
    '''
    print timing information before and after the surrounded context.

    Args: 
        stage_name (str): output label to identify the `stage`.
        additional (str): prints an additional line of information upon entrance.
        logger (callable): the printer, default to the python `print` function, can be altered to any logger api \
            as long as it support basic `print` usage. (i.e. `print(str) -> None`)
        capture (bool): capture `sys.stdout` to add appropriate indentation to all `print` calls.
    '''
    def __init__(self, stage_name: str, additional: Optional[str] = None, logger: Callable[[str], None]=print, capture: bool = False) -> None: 
        self.msg_raw = stage_name
        self.msg = colored(stage_name, 'green', attrs=['bold'])
        self.additional = additional
        self.logger = logger
        self.capture = capture

    def __enter__(self): 
        self.start_time = time.perf_counter()
        self.logger(f'{colored(">", "green")} start [{self.msg}] | on {now_str()}')
        if self.additional is not None: 
            self.logger(f'\t{self.additional}')
        if self.capture: _indent_stdout.increase()
    
    def __exit__(self, _exc_type, _exc_val, _exc_tb): 
        if self.capture: _indent_stdout.decrease()

        elapsed = (time.perf_counter() - self.start_time)
        elapsed_delta = datetime.timedelta(0, elapsed)
        if _exc_tb is not None: 
            msg = colored(self.msg_raw, 'red')
            self.logger(f'{colored("<", "red", attrs=["bold"])} [{msg}] raised an {_exc_type} | on {now_str()} | after {humanize.precisedelta(elapsed_delta)}')
        else : 
            self.logger(f'{colored("<", "green")} done  [{self.msg}] | on {now_str()} | after {humanize.precisedelta(elapsed_delta)}')
        return None




class AggregateVars() : 
    '''
    aggregate all variables local to this context into an iterator
    
    Args: 
        include_self (bool): whether to include the aggregator itself.
    '''

    def __init__(self, include_self = False) : 
        self._Manager_include_self = include_self

    def __enter__(self) : 
        self.upper_list = set(inspect.currentframe().f_back.f_locals.keys())
        self.content = []
        return self

    def __exit__(self, exec_type, exc_val, exc_tb) : 
        new_list = inspect.currentframe().f_back.f_locals.items()
        for k, v in new_list : 
            if (k not in self.upper_list) :
                if isinstance(v,type(self)) : 
                    if getattr(v, '_Manager_include_self') : 
                        self.content.append(v)
                else : 
                    self.content.append(v)

    def __len__(self) : 
        print(len(self.content))

    def __iter__(self) : 
        for v in self.content : 
            yield v

class ColorGradientSerializer(): 
    def __init__(self, 
        value_range: Tuple[float, float] = (0, 1),
        start_color_name: str = '#ff5544', 
        end_color_name: str = '#44aa22', 
        n_gradient: int = 10, 
        alpha: float = 0.5,
        v_gap: float = 0.1,
        n_history: int = 100,
        reverse_gradient: bool = False
    ): 
        if reverse_gradient: 
            start_color_name, end_color_name = end_color_name, start_color_name
        self.palette = {
            str(cid): c.get_hex_l()
            for cid, c in enumerate(colour.Color(start_color_name).range_to(
                colour.Color(end_color_name), n_gradient
            ))
        }

        self.v_range = value_range
        self.n_gradient = n_gradient
        self.alpha = alpha
        self.history = deque(maxlen=n_history)
        self.history.append(value_range[0])
        self.history.append(value_range[1])
    
    def map_value(self, v: float) -> int: 
        s, e = self.v_range
        if v >= e: return self.n_gradient - 1
        if v <= s: return 0
        return int((v - s) / (e - s) * self.n_gradient)
    
    def update_v_range(self, v: float) -> None: 
        self.history.append(v)
        self.v_range = (min(self.history), max(self.history))

    def _print_gradient(self) -> None: 
        import numpy as np
        with colorful.with_palette(self.palette) as C: 
            for (cid, hexname), v in zip(self.palette.items(), np.linspace(*self.v_range, self.n_gradient)): 
                print(getattr(C, cid)(f'{v}: {hexname}'))

    def __call__(self, value: float, format: Optional[str] = None) -> str: 
        with colorful.with_palette(self.palette) as C: 
            res = getattr(C, str(self.map_value(value)))(('%f' if format is None else format)%(value))
        self.update_v_range(value)
        return res


@contextmanager
def move_stdout(f: TextIO): 
    '''temporarily redirect stdout to file `f`
    
    note: not responsible for closing the file `f` on exit!
    '''
    import sys
    saved_stdout = sys.stdout
    sys.stdout = f
    try: 
        yield None
    finally: 
        sys.stdout = saved_stdout

