# author: shiyao
# created: 2021/9/16

from typing import Callable, Iterator

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
    
