# author: shiyao
# created: 2021/9/16

from typing import Callable, Optional, Union, Pattern, List, Dict
from termcolor import colored
from collections import defaultdict
from tool_shack.scripting import ColorGradientSerializer
import time
import re

__all__ = ['TestFunc', 'testcase', 'find_attr']

TestFunc = Callable[[], None]
   
def testcase(should_fail: bool = False): 
    def decorator(func: TestFunc) -> TestFunc: 
        '''
        mark function as a `test case`, and prints basic info at runtime.
        which is a `fn() -> ()` that uses exceptions to mark succ or failure.

        when chained with multiple decorators, this decorator is prefered to be
        placed right next to the original function as it reads the function
        name with the `__name__` attribute.
        '''
        from tool_shack.scripting import StageLogger
        func.test_case_marker = None
        def decorated(): 
            with StageLogger(func.__name__): 
                if should_fail: 
                    try: 
                        func()
                        raise Exception()
                    except Exception: 
                        # sucessfully failed 
                        return
                else: 
                    func()
        return decorated
    return decorator
    
def find_attr(obj: object, pattern: Union[str, Pattern[str]]) -> None: 
    '''print list of matching attribute names associated with `obj`'''

    pat = re.compile(pattern) if isinstance(pattern, str) else pattern
    candidates = (filter(lambda attrname: pat.search(attrname) is not None, dir(obj)))
    
    def ignore_longer(s: Optional[str], n: int) -> str: 
        '''truncate strings longer than n'''
        if s is None: 
            return ''   # early return
        
        s = s.strip()
        if len(s) < n: 
            return s
        else: 
            return s[:n] + '...'
    
    for c in candidates: 
        print(f'{colored(c, "green")} | {ignore_longer(getattr(obj, c).__doc__, 50)}')

_benchmark_logs: Dict[str, List[float]] = defaultdict(lambda: [0])

def benchmark(func): 
    def decorated(*args, **kwargs): 
        start = time.perf_counter()
        res = func(*args, **kwargs)
        end = time.perf_counter()

        elapsed = end - start
        _benchmark_logs[func.__qualname__][0] += 1
        _benchmark_logs[func.__qualname__].append(elapsed)

        return res
    return decorated

def print_benchmark(): 
    import numpy as np 
    collected = []
    for name, logs in _benchmark_logs.items(): 
        log = np.array(logs[1:])
        nc = logs[0]
        collected.append((name, log.mean(), log.std(), log.min(), log.max(), nc))
    
    # sorted by `mean` DESC
    collected.sort(key=lambda x: -x[1])
    painter = ColorGradientSerializer(
        (collected[-1][1], collected[0][1]), 
        reverse_gradient=True
    )

    fmt = '%.3f'
    for name, mean, std, mini, maxi, nc in collected: 
        print(f'{colored(name, attrs=["bold"])}', end='\t| ')
        print(f'{nc} calls, ', end='')
        print(f'elapsed: {painter(mean,fmt)}s±{std:.3f} in [{painter(mini,fmt)} ~ {painter(maxi,fmt)}]s')

    
    


