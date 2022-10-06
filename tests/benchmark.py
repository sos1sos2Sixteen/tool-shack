
import tool_shack.debug as tsd
import random
import time

@tsd.benchmark
def f1(): 
    time.sleep(0.05)
    return 5

@tsd.benchmark
def f2(): 
    time.sleep(0.02)
    return 5

@tsd.benchmark
def f3(): 
    time.sleep(0.01)
    return 5


class A(): 
    @tsd.benchmark
    def ff(self, ):
        time.sleep(0.05 + (random.random()-0.5)*0.1)




if __name__ == '__main__': 
    a = A()
    b = A()
    for _ in range(15): 
        f1()
        f2()
        f3()
        a.ff()
        b.ff()

    
    tsd.print_benchmark()
