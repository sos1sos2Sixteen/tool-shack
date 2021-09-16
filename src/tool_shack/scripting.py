# author: shiyao
# created: 2021/9/16

import time 
import datetime

class StageLogger(): 
    '''
    print timing information before and after the surrounded context.
    
    '''
    def __init__(self, stage_name: str) -> None: 
        self.msg = stage_name

    def now_str(self) -> str: 
        _format = "%Y-%m-%d %H:%M:%S.%f"
        datetime.now().strftime(_format)[:-3]

    def __enter__(self): 
        self.start_time = time.perf_counter()
        print(f'start {self.msg} | on {self.now_str()}')
    
    def __exit__(self, _exc_type, _exc_val, _exc_tb): 
        elapsed_min = (time.perf_counter() - self.start_time) / 60
        print(f'done {self.msg}| took {elapsed_min :.2f} | on {self.now_str()}')