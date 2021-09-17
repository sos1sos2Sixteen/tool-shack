# author: shiyao
# created: 2021/9/16
from functools import reduce
from typing import Sequence, TypeVar, Callable


def _sanity_check(n: int) -> int: 
    '''
    adds the input number by one
    '''
    return n + 1

def now_str() : 
    """
    easily returns current time in human readable format

    use the real `datetime` package if you need sophisticated control over formatting.
    """
    from datetime import datetime
    return datetime.now().strftime("%d %H:%M")


T = TypeVar('T')
E = TypeVar('E')
def tell(teller: Callable[[T], E], x: T) -> T :
    '''
    passing x through, adding an optional side-effet with teller x

    usage: 
    ```
    y = tell(print, x)
    # equals:
    print(x)
    y = x
    ```
    '''
    teller(x)
    return x

def big_and(bools: Sequence[bool]) -> bool: 
    return reduce(lambda a,b : a and b, bools)

T = TypeVar('T')
def contains_all(names: Sequence[T], collection: Sequence[T]) -> bool: 
    '''
    returns whether all items in "names" are in `collection` 
    '''
    return big_and(
        (x in collection) for x in names
    )

class Nullcall : 
    '''
    a class that does absolutely nothing
    '''
    def __call__(self, *args, **kwargs) -> None : 
        pass
    def __getattr__(self, *args, **kwargs) -> "Nullcall" : 
       return self 

    def __getitem__(self, *args, **kwargs) -> "Nullcall" : 
        return self

# an instance of Nullcall (used as a function)
nullcall = Nullcall()

