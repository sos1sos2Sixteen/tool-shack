# author: shiyao
# created: 2021/9/16

from typing import Callable, Optional, Union, Pattern
from termcolor import colored
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