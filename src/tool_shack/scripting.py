# author: shiyao
# created: 2021/9/16

import time 
import datetime
import inspect 
from termcolor import colored
from tool_shack.core import now_str

from typing import Optional

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

class StageLogger(): 
    '''
    print timing information before and after the surrounded context.

    Args: 
        stage_name (str): output label to identify the `stage`.
        additional (str): prints an additional line of information upon entrance.
    '''
    def __init__(self, stage_name: str, additional: Optional[str] = None) -> None: 
        self.msg_raw = stage_name
        self.msg = colored(stage_name, 'green', attrs=['bold'])
        self.additional = additional

    def __enter__(self): 
        self.start_time = time.perf_counter()
        print(f'{colored(">", "green")} start [{self.msg}] | on {now_str()}')
        if self.additional is not None: 
            print(f'\t{self.additional}')
    
    def __exit__(self, _exc_type, _exc_val, _exc_tb): 
        elapsed_min = (time.perf_counter() - self.start_time) / 60
        if _exc_tb is not None: 
            msg = colored(self.msg_raw, 'red')
            print(f'{colored("<", "red", attrs=["bold"])} [{msg}] raised an {_exc_type} | on {now_str()} | after {elapsed_min:.2f}s')
        else : 
            print(f'{colored("<", "green")} done  [{self.msg}] | on {now_str()} | took {elapsed_min :.2f}s')
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

    def __exit__(self, a,b,c) : 
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
